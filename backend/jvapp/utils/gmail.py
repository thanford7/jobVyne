import base64
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
import socket
from typing import Union

# https://github.com/googleapis/google-api-python-client/issues/563
from google.oauth2.credentials import Credentials

from jvapp.utils.oauth import OAUTH_CFGS, OauthProviders

socket.setdefaulttimeout(4000)

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
import oauth2client

from jvapp.utils.datetime import get_datetime_from_unix, get_datetime_or_none

DEFAULT_GMAIL_EMAIL = 'communications@jobvyne.com'
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


@dataclass
class NormalizedEmail:
    employer_id: Union[int, None]
    message_key: str
    thread_key: Union[str, None]
    delivered_to_email: Union[str, None]  # Can be different from to_email if email was forwarded to final destination
    to_email: str
    from_email: str
    subject: str
    body_text: str
    body_html: str
    created_dt: datetime
    
    
class GmailException(Exception):
    pass


class GmailAPIService:
    
    def __init__(self, user_email=DEFAULT_GMAIL_EMAIL):
        from jvapp.models.user import UserSocialCredential  # Avoid circular import
        # oauth2client.client.Credentials.new_from_json
        self.user_email = user_email
        
        # Use service account for jobvyne email addresses
        if re.match('^.*?@jobvyne.com$', user_email):
            credentials = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_GMAIL_CREDENTIALS, scopes=SCOPES
            ).with_subject(self.user_email)
        else:
            google_credentials = UserSocialCredential.objects.filter(
                email=user_email, provider=OauthProviders.google.value
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
        raw_messages = self.get_gmail_messages(lookback_date_str)
        
        message_ids = [m['id'] for m in raw_messages]
        return message_ids

    def get_gmail_messages(self, after_date):
        resp = self.service.users().messages().list(userId=self.user_email, q=f'after:{after_date}').execute()
        return resp.get('messages')

    def get_gmail_message(self, message_id):
        return self.service.users().messages().get(userId=self.user_email, id=message_id).execute()
    
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
        payload = raw_email['payload']
        headers = payload['headers']
        get_header_value_by_name = lambda name: next((h['value'] for h in headers if h['name'] == name), None)
        subject = get_header_value_by_name('Subject')
        subject = subject.replace('[Bad email address] ', '').replace('Re: ', '')
        
        get_body_data = lambda data, mimeType: next((p['body']['data'] for p in data['parts'] if p['mimeType'] == mimeType), None)
        multipart_body = next((p for p in payload['parts'] if p['mimeType'] == 'multipart/alternative'), None)
        if multipart_body:
            raw_body_text = get_body_data(multipart_body, 'text/plain')
            raw_body_html = get_body_data(multipart_body, 'text/html')
        else:
            raw_body_text = get_body_data(payload, 'text/plain')
            raw_body_html = get_body_data(payload, 'text/html')

        body_text = base64.urlsafe_b64decode(raw_body_text).decode('utf-8') if raw_body_text else None
        # Get rid of the past message history. We just want the most recent message text
        if body_text:
            body_text = re.sub('On .*?wrote:.*', '', body_text, flags=re.DOTALL)
        
        to_email = self.get_email_address_from_header(get_header_value_by_name('To'))
        employer_match = re.match('^communications_(?P<employer_id>[0-9]+)@jobvyne\.com$', to_email)
        employer_id = None
        if employer_match:
            employer_id = int(employer_match.group('employer_id'))
        
        # TODO: Add attachments
        return NormalizedEmail(
            employer_id=employer_id,
            message_key=raw_email['id'],
            thread_key=raw_email['threadId'],
            delivered_to_email=self.get_email_address_from_header(get_header_value_by_name('Delivered-To')),
            to_email=to_email,
            from_email=self.get_email_address_from_header(get_header_value_by_name('From')),
            subject=subject,
            body_text=body_text,
            body_html=base64.urlsafe_b64decode(raw_body_html).decode('utf-8') if raw_body_html else None,
            created_dt=get_datetime_from_unix(raw_email['internalDate'], is_in_ms=True)
        )
    
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
