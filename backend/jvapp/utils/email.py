import base64
import logging
import os
from urllib.request import urlopen

from django.conf import settings
from django.template import loader
from django.templatetags.static import static
from sendgrid import SendGridAPIClient, Attachment, ContentId, Disposition, FileType, FileName, FileContent
from sendgrid.helpers.mail import Mail

from jvapp.utils.logger import getLogger

EMAIL_ADDRESS_TEST = 'test@jobvyne.com'
EMAIL_ADDRESS_SEND = 'no-reply@jobvyne.com'  # Email address where all emails originate from
EMAIL_ADDRESS_SUPPORT = 'support@jobvyne.com'
EMAIL_ADDRESS_SALES = 'sales@jobvyne.com'
EMAIL_ADDRESS_MARKETING = 'marketing@jobvyne.com'
sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
logger = getLogger()


# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
def send_sg_email(message: Mail):
    try:
        response = sg.send(message)
        return response
    except Exception as e:
        logger.log(logging.ERROR, f'{e.status_code} {e.reason}: {e.body}')
        return False


def get_encoded_file(fileUrl):
    file_openner = lambda url: urlopen(url)
    if settings.DEBUG:
        file_openner = lambda url: open(url, 'rb')
    with file_openner(fileUrl) as file:
        encoded_file = base64.b64encode(file.read()).decode()
    return encoded_file


def get_attachment(file_name, file_url, file_type, content_id, is_display_inline=False):
    encodedLogo = get_encoded_file(file_url)
    
    return Attachment(
        file_content=FileContent(encodedLogo),
        file_name=FileName(file_name),
        file_type=FileType(file_type),
        disposition=Disposition('inline') if is_display_inline else None,
        content_id=ContentId(content_id)
    )


def send_email(subject_text, to_emails, django_context=None, django_email_body_template=None, html_content=None,
              from_email=None, cc_email=None, attachments=None):
    """Blend SendGrid's email service with Django's email templates
    :param subject_text {str}: The email subject line
    :param to_emails {list}:
    :param django_context {dict}: Key/value pairs that can be accessed in the djangoEmailBody
    :param django_email_body_template {str}: Email template path to be used for the body. Can be null if htmlContent is
    provided directly
    :param html_content {str}: Html string that has already been formatted
    :param from_email {str}: If not provided, the default no reply email will be used
    :param attachments {list}: Each attachment must be an Attachment object
    :return: SendGrid email response
    """
    subject = ''.join(subject_text.splitlines())  # Email subject *must not* contain newlines
    if os.getenv('DB') != 'prod':
        subject = '(Test) ' + subject
    django_context = django_context or {}
    django_context['support_email'] = EMAIL_ADDRESS_SUPPORT
    htmlContent = html_content or loader.render_to_string(django_email_body_template, django_context)
    
    message = Mail(
        from_email=from_email or EMAIL_ADDRESS_SEND,
        to_emails=to_emails if not settings.DEBUG else EMAIL_ADDRESS_TEST,
        subject=subject,
        html_content=htmlContent)
    
    if cc_email and not settings.DEBUG:
        if not isinstance(cc_email, list):
            cc_email = [cc_email]
        for email in cc_email:
            message.add_cc(email)
    
    # Add JobVyne logo
    image_url = static('jobVyneLogo.png')
    message.attachment = get_attachment(
        'logo.png',
        image_url,
        'image/png',
        'logo',
        is_display_inline=True
    )
    
    if attachments:
        for attachment in attachments:
            message.attachment = attachment
    
    return send_sg_email(message)