import logging
import os
import re
from email.mime.image import MIMEImage

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.templatetags.static import static
from django.utils.html import strip_tags

IS_PRODUCTION = os.getenv('DB') == 'prod'
EMAIL_ADDRESS_TEST = 'test@jobvyne.com'
EMAIL_ADDRESS_SEND = 'no-reply@jobvyne.com'  # Email address where all emails originate from
EMAIL_ADDRESS_SUPPORT = 'support@jobvyne.com'
EMAIL_ADDRESS_SALES = 'sales@jobvyne.com'
EMAIL_ADDRESS_MARKETING = 'marketing@jobvyne.com'
logger = logging.getLogger(__name__)


def send_django_email(subject_text, to_emails, django_context=None, django_email_body_template=None, html_content=None,
                      from_email=None, cc_email=None, files=None):
    if not settings.IS_SEND_EMAILS:
        return
    subject = ''.join(subject_text.splitlines())  # Email subject *must not* contain newlines
    django_context = django_context or {}
    django_context['support_email'] = EMAIL_ADDRESS_SUPPORT
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
    
    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_content,
        from_email=from_email or EMAIL_ADDRESS_SEND,
        to=to_emails,
        cc=cc_email
    )
    message.attach_alternative(html_content, "text/html")

    with open(static('jobVyneLogo.png'), 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    message.attach(logo)
    
    if files:
        for f in files:
            # File might be an in-memory file that has just been uploaded or a
            # file that is attached to a model instance. If it is attached to a
            # model instance, we attach it using the path to the file which will
            # be a string value
            if isinstance(f, str):
                message.attach_file(f)
            else:
                message.attach(f.name, f.read(), f.content_type)
    
    return message.send()


def get_domain_from_email(email):
    email = email.strip()
    domain_regex = re.compile('(?P<domain>[0-9a-z-]+?\.[0-9a-z-]+$)', re.I)
    email_match = re.search(domain_regex, email)
    if not email_match:
        return None
    return email_match.group('domain')
