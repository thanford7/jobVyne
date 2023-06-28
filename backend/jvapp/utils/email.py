import json
import logging
import os
import re
from email.mime.image import MIMEImage
from enum import Enum
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.transaction import atomic
from django.template import loader
from django.templatetags.static import static
from django.utils import timezone

from jvapp.models.tracking import Message, MessageAttachment, MessageRecipient
from jvapp.utils.file import get_file_name, get_safe_file_path
from jvapp.utils.gmail import GmailAPIService

IS_PRODUCTION = os.getenv('DB') == 'prod'
MESSAGE_ID_KEY = 'jv_message_id'
MESSAGE_ENVIRONMENT_KEY = 'jv_base_url'
EMAIL_ADDRESS_SEND = 'no-reply@jobvyne.com'  # Email address where all emails originate from
EMAIL_ADDRESS_COMMUNICATION = f'{settings.COMMUNICATION_ADDRESS}@jobvyne.com'  # Bi-directional email for users to correspond
EMAIL_ADDRESS_SUPPORT = 'support@jobvyne.com'
EMAIL_ADDRESS_SALES = 'sales@jobvyne.com'
EMAIL_ADDRESS_MARKETING = 'marketing@jobvyne.com'
ALLOWED_LOCAL_EMAIL_ADDRESSES = [
    EMAIL_ADDRESS_SEND, EMAIL_ADDRESS_COMMUNICATION, EMAIL_ADDRESS_SUPPORT,
    EMAIL_ADDRESS_SALES, EMAIL_ADDRESS_MARKETING, 'thanford7@gmail.com'
]
logger = logging.getLogger(__name__)


# Keep in sync with EmailUtil on frontend
class ContentPlaceholders(Enum):
    APPLICANT_FIRST_NAME = '{{applicant.first_name}}'
    APPLICANT_LAST_NAME = '{{applicant.last_name}}'
    JOB_LINK = '{{link}}'
    JOB_TITLE = '{{job.job_title}}'
    JOBS_LIST = '{{jobs-list}}'
    EMPLOYEE_FIRST_NAME = '{{employee.first_name}}'
    EMPLOYEE_LAST_NAME = '{{employee.last_name}}'
    EMPLOYER_NAME = '{{employer.name}}'


def get_file_from_path(file_path):
    is_url = bool(re.match('^http', file_path))
    file_opener = urlopen if is_url else lambda f: open(f, 'rb')
    with file_opener(file_path) as file:
        file_data = file.read()
    return file_data

@atomic
def send_django_email(
    subject_text, django_email_body_template,
    to_email=None, cc_email=None, bcc_email=None, from_email=EMAIL_ADDRESS_SEND,
    django_context=None, html_body_content=None, employer=None, is_include_jobvyne_subject=True,
    files=None, message_thread=None, is_tracked=True, is_gmail=False
):
    if not settings.IS_SEND_EMAILS:
        return
    
    if not any((to_email, cc_email, bcc_email)):
        logger.warning('At least one email recipient is required')
        return
    
    subject = ''.join(subject_text.splitlines())  # Email subject *must not* contain newlines
    if is_include_jobvyne_subject:
        subject = f'🍇 JobVyne | {subject}'
    django_context = django_context or {}
    django_context['support_email'] = EMAIL_ADDRESS_SUPPORT
    django_context['base_url'] = settings.BASE_URL
    django_context['protocol'] = 'https'  # Overwrite protocol to always use https
    django_context['html_body_content'] = html_body_content
    django_context['is_employer_logo'] = bool(employer)
    django_context['employer_name'] = employer.employer_name if employer else None
    html_content = loader.render_to_string(django_email_body_template, django_context)
    plain_content = BeautifulSoup(html_content).get_text(strip=True, separator=' ')
    
    # Make sure emails aren't sent to actual people when not in production
    if not any([
        IS_PRODUCTION,
        to_email in settings.DEV_EMAILS
    ]):
        subject = '(Test) ' + subject
        logger.info(
            f'Sending email to test address. This email would have been sent to {to_email}, cced to {cc_email}, and bcced to {bcc_email}')
        if cc_email:
            cc_email = [settings.EMAIL_ADDRESS_TEST]
        if bcc_email:
            bcc_email = [settings.EMAIL_ADDRESS_TEST]
        to_email = [settings.EMAIL_ADDRESS_TEST]
        if (from_email not in ALLOWED_LOCAL_EMAIL_ADDRESSES) and not re.match('^communications.*?@jobvyne\.com$', from_email):
            from_email = EMAIL_ADDRESS_SEND
    
    if cc_email and not isinstance(cc_email, list):
        cc_email = [cc_email]
        
    if bcc_email and not isinstance(bcc_email, list):
        bcc_email = [bcc_email]
    
    if not isinstance(to_email, list):
        to_email = [to_email]
    
    # Save messages to the database so we can track delivery
    jv_message = None
    message_attachments = None
    if is_tracked:
        jv_message = Message(
            type=Message.MessageType.EMAIL.value,
            subject=subject,
            body=BeautifulSoup(html_body_content).get_text(strip=True, separator=' ') if html_body_content else plain_content,
            body_html=html_content,
            from_address=from_email,
            created_dt=timezone.now(),
            message_thread=message_thread
        )
        jv_message.save()
        recipients = []
        for recipient_type, recipient_emails in (
            (MessageRecipient.RecipientType.TO.value, to_email or []),
            (MessageRecipient.RecipientType.CC.value, cc_email or []),
            (MessageRecipient.RecipientType.BCC.value, bcc_email or [])
        ):
            for recipient_email in recipient_emails:
                # Add error upfront incase email is never sent. Remove error once sent
                recipients.append(MessageRecipient(
                    message=jv_message,
                    recipient_address=recipient_email,
                    recipient_type=recipient_type,
                    error_dt=timezone.now(),
                    error_reason='UNSENT'
                ))
        MessageRecipient.objects.bulk_create(recipients)
        message_attachments = []
        for f in (files or []):
            message_attachments.append(MessageAttachment(
                message=jv_message,
                file=f
            ))
        MessageAttachment.objects.bulk_create(message_attachments)
    
    # Send the actual email
    email_cfg = {
        'subject': subject,
        'body': plain_content,
        'from_email': from_email,
        'to': to_email,
        'cc': cc_email,
        'bcc': bcc_email
    }
    if is_tracked:
        email_cfg['reply_to'] = [from_email, f'{settings.COMMUNICATION_ADDRESS}_{jv_message.id}@jobvyne.com']
        email_cfg['headers'] = {
            'X-SMTPAPI': json.dumps({'unique_args': {MESSAGE_ID_KEY: jv_message.id, MESSAGE_ENVIRONMENT_KEY: settings.BASE_URL}})
        }
    message = EmailMultiAlternatives(**email_cfg)
    message.attach_alternative(html_content, "text/html")

    logo = MIMEImage(get_file_from_path(static('jobVyneLogo.png')))
    logo.add_header('Content-ID', '<jobvyne_logo>')
    message.attach(logo)
    
    if employer and employer.logo:
        file_path = get_safe_file_path(employer.logo)
        subtype = None
        if re.match('^.*\.(jpeg|jpg)$', file_path):
            subtype = 'jpeg'
        employer_logo = MIMEImage(get_file_from_path(file_path), _subtype=subtype)
        employer_logo.add_header('Content-ID', '<employer_logo>')
        message.attach(employer_logo)
        
    if is_tracked:
        # Note: Need to use message_attachments instead of files since in-memory files
        # have already been read and will return b'' if attempted to read again
        for attachment in message_attachments:
            file_path = get_safe_file_path(attachment.file)
            message.attach(get_file_name(file_path), get_file_from_path(file_path))
    else:
        for f in (files or []):
            message.attach(f.name, f.read())
    
    message_id = None
    num_sent = None
    if is_gmail:
        gmail_api = GmailAPIService(user_email=from_email)
        message_id, thread_id = gmail_api.send_gmail_message(message.message())
        if jv_message:
            jv_message.external_message_key = message_id
            jv_message.save()
        # Save google message thread to track further emails
        if message_thread and not message_thread.external_thread_key:
            message_thread.external_thread_key = thread_id
            message_thread.save()
    else:
        num_sent = message.send()
        
    # Successfully sent message
    if jv_message and (message_id or num_sent):
        recipients = MessageRecipient.objects.filter(message=jv_message)
        for recipient in recipients:
            recipient.error_dt = None
            recipient.error_reason = None
        
        MessageRecipient.objects.bulk_update(recipients, ['error_dt', 'error_reason'])
    
    return message_id or num_sent


def get_domain_from_email(email):
    email = email.strip()
    domain_regex = re.compile('(?P<domain>[0-9a-z-]+?\.[0-9a-z-]+$)', re.I)
    email_match = re.search(domain_regex, email)
    if not email_match:
        return None
    return email_match.group('domain')
