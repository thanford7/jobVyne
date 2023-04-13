import base64
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
import socket
from itertools import groupby
from typing import Union

# https://github.com/googleapis/google-api-python-client/issues/563
from google.oauth2.credentials import Credentials

from jvapp.utils.oauth import OAUTH_CFGS, OauthProviders

socket.setdefaulttimeout(4000)

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build

from jvapp.utils.datetime import get_datetime_from_unix, get_datetime_or_none

DEFAULT_GMAIL_EMAIL = 'communications@jobvyne.com'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


@dataclass
class NormalizedEmail:
    message_key: str
    thread_key: Union[str, None]
    delivered_to_email: Union[str, None]  # Can be different from to_email if email was forwarded to final destination
    to_emails: list
    from_email: str
    subject: str
    body_text: str
    body_html: str
    created_dt: datetime
    attachment_files: list
    
    
class GmailException(Exception):
    pass


class GmailAPIService:
    
    def __init__(self, user_email=DEFAULT_GMAIL_EMAIL):
        # oauth2client.client.Credentials.new_from_json
        self.user_email = user_email
        self.set_service()
        
    def set_service(self):
        from jvapp.models.user import UserSocialCredential  # Avoid circular import
        # Use service account for jobvyne email addresses
        if re.match('^.*?@jobvyne.com$', self.user_email):
            credentials = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_GMAIL_CREDENTIALS, scopes=SCOPES
            ).with_subject(self.user_email)
        else:
            google_credentials = UserSocialCredential.objects.filter(
                email=self.user_email, provider=OauthProviders.google.value
            )
            if not google_credentials:
                raise GmailException('This user is has not authenticated their Gmail account')
            credentials = self.get_credentials(google_credentials[0])
    
        self.service = build('gmail', 'v1', credentials=credentials)
        
    def start_pub_sub_watch(self):
        # Watcher must be refreshed at least every 7 days
        # https://developers.google.com/gmail/api/guides/push#watch_request
        
        request = {
          'labelIds': ['INBOX'],
          'topicName': 'projects/jobvyne-prod-357017/topics/gmail'
        }
        return self.service.users().watch(userId=self.user_email, body=request).execute()
    
    def get_new_message_ids_from_pub_sub(self, request):
        # Note: the historyId in the pub/sub message is not the latestHistoryId for email
        # This is why a lookback period is used instead
        publish_date = get_datetime_or_none(request.data['message']['publishTime'], as_date=True)
        lookback_date_str = (publish_date - timedelta(days=1)).strftime('%Y/%m/%d')
        try:
            raw_messages = self.get_gmail_messages(lookback_date_str)
        except TimeoutError:
            self.set_service()
            raw_messages = self.get_gmail_messages(lookback_date_str)
        
        message_ids = [m['id'] for m in raw_messages]
        return message_ids

    def get_gmail_messages(self, after_date):
        resp = self.service.users().messages().list(userId=self.user_email, q=f'after:{after_date}').execute()
        return resp.get('messages')

    def get_gmail_message(self, message_id):
        return self.service.users().messages().get(userId=self.user_email, id=message_id).execute()
    
    def get_message_attachment(self, message_id, attachment_id):
        raw_attachment = self.service.users().messages().attachments().get(
            userId=self.user_email, messageId=message_id, id=attachment_id
        ).execute()
        if not raw_attachment['data']:
            return None
        return base64.urlsafe_b64decode(raw_attachment['data'])
    
    def get_message_thread(self, thread_id):
        return self.service.users().threads().get(userId=self.user_email, id=thread_id).execute()
    
    def get_user_history(self, history_id):
        return self.service.users().history().list(userId=self.user_email, startHistoryId=history_id).execute()

    def send_gmail_message(self, message):
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()
    
        create_message = {
            'raw': encoded_message
        }
        resp = self.service.users().messages().send(userId=self.user_email, body=create_message).execute()
        message_id = resp['id']
        thread_id = resp['threadId']
        return message_id, thread_id
    
    def decode_pub_sub_message(self, data):
        decoded_data = base64.b64decode(data)
        # {"emailAddress": "user@example.com", "historyId": "9876543210"}
        return json.loads(decoded_data)
    
    def get_normalized_email(self, raw_email):
        from jvapp.models import Message  # Avoid circular import
        payload = raw_email['payload']
        headers = payload['headers']
        get_header_value_by_name = lambda name: next((h['value'] for h in headers if h['name'] == name), None)
        subject = get_header_value_by_name('Subject')
        subject = subject.replace('[Bad email address] ', '').replace('Re: ', '')
        
        parts_by_mimetype = {}
        for mimeType, parts in groupby(self.get_message_parts(payload), lambda x: x['mimeType']):
            parts_by_mimetype[mimeType] = list(parts)
        
        body_text = ''
        for part in parts_by_mimetype['text/plain']:
            if part['body']['data']:
                body_text += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8').strip()
                
        body_html = ''
        for part in parts_by_mimetype['text/html']:
            if part['body']['data']:
                body_html += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8').strip()

        # Get rid of the past message history. We just want the most recent message text
        if body_text:
            body_text = re.sub('On .*?wrote:.*', '', body_text, flags=re.DOTALL)

        to_emails = [
            email.strip() for email
            in self.get_email_address_from_header(get_header_value_by_name('To')).split(',')
        ]

        thread_key = None
        final_to_emails = []
        for email in to_emails:
            message_match = re.match('^communications_(?P<message_id>[0-9]+)@jobvyne\.com$', email)
            if message_match:
                message_id = int(message_match.group('message_id'))
                try:
                    message = Message.objects.select_related('message_thread').get(id=message_id)
                    thread_key = message.message_thread.external_thread_key
                except Message.DoesNotExist:
                    pass
            else:
                final_to_emails.append(email)
            
        # attachments
        attachment_files = []
        for parts in parts_by_mimetype.values():
            for part in parts:
                if part.get('filename') and part['filename'] != 'noname' and part['body'].get('attachmentId'):
                    attachment_files.append({'id': part['body']['attachmentId'], 'name': part['filename']})
        
        return NormalizedEmail(
            message_key=raw_email['id'],
            thread_key=thread_key or raw_email['threadId'],
            delivered_to_email=self.get_email_address_from_header(get_header_value_by_name('Delivered-To')),
            to_emails=[email for email in final_to_emails if email != DEFAULT_GMAIL_EMAIL],
            from_email=self.get_email_address_from_header(get_header_value_by_name('From')),
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            created_dt=get_datetime_from_unix(raw_email['internalDate'], is_in_ms=True),
            attachment_files=attachment_files
        )
    
    @staticmethod
    def get_message_parts(payload):
        parts = []
        for part in payload['parts']:
            if part.get('parts'):
                parts += GmailAPIService.get_message_parts(part)
            else:
                parts.append(part)
        return parts
        
    
    @staticmethod
    def get_email_address_from_header(raw_email):
        if not raw_email:
            return None
        for pattern in ('^.*?<(?P<email>.+?@.+?)>$', '(?P<email>.+?@.+?)$'):
            match = re.match(pattern, raw_email)
            if match:
                return match.group('email')
        
        return None
    
    @staticmethod
    def get_credentials(user_social_credential):
        google_oauth_cfg = OAUTH_CFGS[OauthProviders.google.value]
        return Credentials(
            user_social_credential.access_token,
            refresh_token=user_social_credential.refresh_token,
            token_uri=google_oauth_cfg['token_url'],
            client_id=google_oauth_cfg['auth_params']['client_id'],
            client_secret=settings.SOCIAL_AUTH_GOOGLE_SECRET,
            scopes=google_oauth_cfg['auth_params']['scope']
        )
