from enum import Enum

from django.db import models
from django.db.models import Q
from django.utils import timezone

from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin

__all__ = ('PageView', 'Message', 'MessageRecipient', 'MessageAttachment', 'MessageThread', 'MessageThreadContext')


class PageView(models.Model, JobVynePermissionsMixin):
    # page
    relative_url = models.CharField(max_length=100)
    social_link_filter = models.ForeignKey(
        'SocialLinkFilter', on_delete=models.CASCADE, null=True, blank=True, related_name='page_view'
    )
    platform = models.ForeignKey('SocialPlatform', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Unique characteristics
    ip_address = models.CharField(max_length=40, null=True, blank=True)
    access_dt = models.DateTimeField(default=timezone.now)
    
    # location
    city = models.CharField(max_length=60, null=True, blank=True)
    country = models.CharField(max_length=60, null=True, blank=True)
    region = models.CharField(max_length=60, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    
    # user agent
    browser = models.CharField(max_length=60, null=True, blank=True)
    browser_version = models.CharField(max_length=20, null=True, blank=True)
    operating_system = models.CharField(max_length=30, null=True, blank=True)
    device_type = models.CharField(max_length=40, null=True, blank=True)
    device_brand = models.CharField(max_length=40, null=True, blank=True)
    device_model = models.CharField(max_length=40, null=True, blank=True)
    is_mobile = models.BooleanField(null=True, blank=True)
    is_tablet = models.BooleanField(null=True, blank=True)
    is_pc = models.BooleanField(null=True, blank=True)
    is_bot = models.BooleanField(null=True, blank=True)

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
    
        filter = Q(social_link_filter__owner_id=user.id)
        if user.is_employer:
            filter |= Q(social_link_filter__employer_id=user.employer_id)
    
        return query.filter(filter)
    
    
class Message(models.Model):
    class MessageType(Enum):
        EMAIL = 'email'
        SMS = 'text'
    
    type = models.CharField(max_length=5)
    subject = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    body_html = models.TextField(null=True, blank=True)
    from_user = models.ForeignKey('JobVyneUser', null=True, blank=True, on_delete=models.SET_NULL, related_name='outgoing_message')
    from_address = models.CharField(max_length=255)
    created_dt = models.DateTimeField()
    # TODO: Limit message sub thread depth to one level
    message_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    message_thread = models.ForeignKey('MessageThread', null=True, blank=True, on_delete=models.PROTECT, related_name='message')
    
    class Meta:
        ordering = ('-created_dt',)


class MessageAttachment(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='attachment')
    file = models.FileField(upload_to='message_attachments')
    
    
class MessageRecipient(models.Model):
    class RecipientType(Enum):
        TO = 'to'
        CC = 'cc'
        BCC = 'bcc'
    
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='recipient')
    recipient_user = models.ForeignKey('JobVyneUser', null=True, blank=True, on_delete=models.SET_NULL, related_name='message_recipient')
    recipient_address = models.CharField(max_length=255)
    recipient_type = models.CharField(max_length=3, default=RecipientType.TO.value)
    provider_message_key = models.CharField(max_length=80, null=True, blank=True)
    processed_dt = models.DateTimeField(null=True, blank=True)
    error_dt = models.DateTimeField(null=True, blank=True)
    delivered_dt = models.DateTimeField(null=True, blank=True)
    opened_dt = models.DateTimeField(null=True, blank=True)
    clicked_dt = models.DateTimeField(null=True, blank=True)
    error_reason = models.CharField(max_length=500, null=True, blank=True)
    

class MessageThread(models.Model):
    """ Group messages into a thread. Any entities added to a message thread will
    have access to the messages within the thread. This is helpful, for example, if
    multiple HR users are messaging with a job candidate.
    """
    message_groups = models.ManyToManyField('MessageGroup')
    
    
class MessageThreadContext(models.Model):
    """ Allows message threads to be accessible from related models. For example, if a message
    thread is about a job application, it can be accessed through the JobApplication model. Ability
    to see the message thread is managed through the MessageThread. For example:
        MessageThread.employer = Google
        MessageThreadContext.applicant = Jack Dorsey
        This message thread can be filtered based on the applicant and should be accessible
        by Google employer users, but not the applicant
    """
    message_thread = models.OneToOneField('MessageThread', on_delete=models.CASCADE, related_name='message_thread_context')
    job_application = models.ForeignKey('JobApplication', on_delete=models.SET_NULL, null=True, blank=True, related_name='message_thread_context')
    job = models.ForeignKey('EmployerJob', on_delete=models.SET_NULL, null=True, blank=True, related_name='message_thread_context')
    applicant = models.ForeignKey('JobVyneUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='message_thread_context')


class MessageGroup(AuditFields):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, null=True, blank=True)
    user_type_bits = models.SmallIntegerField(default=0)
    users = models.ManyToManyField('JobVyneUser')
    
    def get_key(self):
        users = self.users.all()
        if users:
            user_ids = tuple(sorted([u.id for u in users]))
        else:
            user_ids = None
        return self.employer_id, self.user_type_bits, user_ids
    
    def is_same(self, message_group):
        return self.get_key() == message_group.get_key()
    
    @classmethod
    def get_key_from_data(cls, user_ids, employer_id, user_type_bits):
        if user_ids:
            sorted_user_ids = tuple(sorted(user_ids))
        else:
            sorted_user_ids = None
        return employer_id, user_type_bits, sorted_user_ids
    
    @classmethod
    def is_valid_instance(cls, user_ids, employer_id):
        """Make sure user group is not too permissive. There must be at least
        one user or employer
        """
        return bool(user_ids or employer_id)
