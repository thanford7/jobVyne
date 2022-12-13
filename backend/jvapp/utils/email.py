import json
import logging
import os
import re
from email.mime.image import MIMEImage

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.templatetags.static import static
from django.utils import timezone
from django.utils.html import strip_tags

from jvapp.models.tracking import Message, MessageAttachment, MessageRecipient

IS_PRODUCTION = os.getenv('DB') == 'prod'
MESSAGE_ID_KEY = 'jv_message_id'
MESSAGE_ENVIRONMENT_KEY = 'jv_base_url'
EMAIL_ADDRESS_TEST = 'test@jobvyne.com'
EMAIL_ADDRESS_SEND = 'no-reply@jobvyne.com'  # Email address where all emails originate from
EMAIL_ADDRESS_SUPPORT = 'support@jobvyne.com'
EMAIL_ADDRESS_SALES = 'sales@jobvyne.com'
EMAIL_ADDRESS_MARKETING = 'marketing@jobvyne.com'
logger = logging.getLogger(__name__)


def send_django_email(subject_text, to_emails, django_context=None, django_email_body_template=None, html_content=None,
                      from_email=EMAIL_ADDRESS_SEND, cc_email=None, files=None, message_thread=None):
    if not settings.IS_SEND_EMAILS:
        return
    subject = ''.join(subject_text.splitlines())  # Email subject *must not* contain newlines
    django_context = django_context or {}
    django_context['support_email'] = EMAIL_ADDRESS_SUPPORT
    django_context['base_url'] = settings.BASE_URL
    django_context['protocol'] = 'https'  # Overwrite protocol to always use https
    html_content = html_content or loader.render_to_string(django_email_body_template, django_context)
    plain_content = strip_tags(html_content)
    
    if not IS_PRODUCTION:
        subject = '(Test) ' + subject
        logger.info(
            f'Sending email to test address. This email would have been sent to {to_emails} and cced to {cc_email}')
        if cc_email:
            cc_email = [EMAIL_ADDRESS_TEST]
        to_emails = [EMAIL_ADDRESS_TEST]
    
    if cc_email and not isinstance(cc_email, list):
        cc_email = [cc_email]
    
    if not isinstance(to_emails, list):
        to_emails = [to_emails]
    
    # Save messages to the database so we can track delivery
    jv_message = Message(
        type=Message.MessageType.EMAIL.value,
        subject=subject,
        body=plain_content,
        body_html=html_content,
        from_address=from_email,
        created_dt=timezone.now(),
        message_thread=message_thread
    )
    jv_message.save()
    recipients = []
    for recipient_email in to_emails + (cc_email or []):
        recipients.append(MessageRecipient(
            message=jv_message,
            recipient_address=recipient_email
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
    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_content,
        from_email=from_email,
        to=to_emails,
        cc=cc_email,
        headers={
            'X-SMTPAPI': json.dumps({'unique_args': {MESSAGE_ID_KEY: jv_message.id, MESSAGE_ENVIRONMENT_KEY: settings.BASE_URL}})
        }
    )
    message.attach_alternative(html_content, "text/html")

    with open(static('jobVyneLogo.png'), 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    message.attach(logo)
    
    # Note: Need to use message_attachments instead of files since in-memory files
    # have already been read and will return b'' if attempted to read again
    for attachment in message_attachments:
        message.attach_file(attachment.file.path)
    
    return message.send()


def get_domain_from_email(email):
    email = email.strip()
    domain_regex = re.compile('(?P<domain>[0-9a-z-]+?\.[0-9a-z-]+$)', re.I)
    email_match = re.search(domain_regex, email)
    if not email_match:
        return None
    return email_match.group('domain')
