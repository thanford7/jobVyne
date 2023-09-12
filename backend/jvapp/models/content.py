from enum import Enum

from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q, UniqueConstraint

from jvapp.models.abstract import ALLOWED_UPLOADS_IMAGE, ALLOWED_UPLOADS_VIDEO, AuditFields, JobVynePermissionsMixin

__all__ = ('Article', 'ContentType', 'ContentItem', 'SocialContentItem', 'SocialPost', 'SocialPostFile', 'SocialPostAudit')

from jvapp.models.employer import Taxonomy

from jvapp.models.user import PermissionName


def get_post_upload_location(instance, filename):
    if instance.social_post.user_id:
        return f'user/{instance.social_post.user.email}/{filename}'
    elif instance.social_post.employer_id:
        return f'employers/{instance.social_post.employer_id}/{filename}'
    return 'social-posts'


class ContentType(Enum):
    TEXT = 'TEXT'
    ICON = 'ICON',
    CAROUSEL = 'CAROUSEL'
    ACCORDION = 'ACCORDION'
    MESSAGE = 'MESSAGE'


class ContentItem(AuditFields):
    header = models.CharField(max_length=250, null=True, blank=True)
    orderIdx = models.SmallIntegerField(null=True, blank=True)
    type = models.CharField(max_length=15)
    config = models.JSONField(null=True, blank=True)
    item_parts = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ('orderIdx', )


class SocialContentItem(models.Model, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', null=True, blank=True, on_delete=models.CASCADE, related_name='social_content_item')
    user = models.ForeignKey('JobVyneUser', null=True, blank=True, on_delete=models.CASCADE, related_name='social_content_item')
    content = models.TextField()

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        filter = Q(employer_id=user.employer_id) | Q(user_id=user.id)
        return query.filter(filter)
    
    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_CONTENT.value, user.employer_id)
            )
            or (
                self.user_id == user.id
                and ((not user.employer_id) or user.has_employer_permission(PermissionName.ADD_EMPLOYEE_CONTENT.value, user.employer_id))
            )
        )


class SocialPost(AuditFields, JobVynePermissionsMixin):
    employer = models.ForeignKey('Employer', null=True, blank=True, on_delete=models.CASCADE, related_name='social_post')
    user = models.ForeignKey('JobVyneUser', null=True, blank=True, on_delete=models.CASCADE, related_name='social_post')
    content = models.TextField()
    original_post = models.ForeignKey('SocialPost', null=True, blank=True, on_delete=models.SET_NULL, related_name='child_post')
    post_credentials = models.ManyToManyField('UserSocialCredential')
    social_link = models.ForeignKey('SocialLink', null=True, blank=True, on_delete=models.SET_NULL)
    is_auto_post = models.BooleanField(default=False)
    auto_start_dt = models.DateTimeField(null=True, blank=True)
    auto_weeks_between = models.SmallIntegerField(null=True, blank=True)
    auto_day_of_week = models.SmallIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ('-created_dt',)

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
    
        filter = Q(employer_id=user.employer_id) | Q(user_id=user.id)
        return query.filter(filter)

    def _jv_can_create(self, user):
        return (
            user.is_admin
            or (
                self.employer_id == user.employer_id
                and user.has_employer_permission(PermissionName.MANAGE_EMPLOYER_CONTENT.value, user.employer_id)
            )
            or self.user_id == user.id
        )
    

class SocialPostFile(models.Model):
    social_post = models.ForeignKey('SocialPost', on_delete=models.CASCADE, related_name='file')
    file = models.FileField(
        upload_to=get_post_upload_location,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_VIDEO + ALLOWED_UPLOADS_IMAGE)]
    )


class SocialPostAudit(models.Model):
    social_post = models.ForeignKey('SocialPost', on_delete=models.CASCADE, related_name='audit')
    formatted_content = models.TextField()
    email = models.EmailField()
    platform = models.CharField(max_length=20)
    posted_dt = models.DateTimeField()
    
    class Meta:
        ordering = ('-posted_dt',)


class JobPost(AuditFields):
    """Keep track of which jobs have been posted to specific channels so they are only posted
    once. Differs from SocialPost because here we are tracking individual jobs whereas a social
    post includes a referral link which may show the same job multiple times
    """
    # Keep in sync with SocialUtil
    class PostChannel(Enum):
        # Sent to professional orgs for candidates to apply to jobs
        SLACK_JOB = 'slack-job'
        # Sent to employees to ask them to refer for a specific job
        SLACK_EMPLOYEE_REFERRAL = 'slack-employee-referral'
        LINKEDIN_JOB = 'linkedin-job'
    
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, null=True, blank=True, related_name='job_post')
    # Owner indicates an "influencer" that posted to a channel
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, null=True, blank=True, related_name='job_post')
    # Recipient indicates a job seeker that received a job post to a channel
    recipient = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, null=True, blank=True, related_name='recipient_job_post')
    job = models.ForeignKey('EmployerJob', on_delete=models.CASCADE, related_name='job_post')
    channel = models.CharField(max_length=30)
    meta_data = models.JSONField(blank=True, null=True)  # Useful for storing responses, original message text, etc
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['employer', 'job', 'channel'],
                condition=Q(owner=None, recipient=None),
                name='unique_employer_job_channel'
            ),
            UniqueConstraint(
                fields=['owner', 'job', 'channel'],
                condition=Q(employer=None, recipient=None),
                name='unique_owner_job_channel'
            ),
            UniqueConstraint(
                fields=['recipient', 'job', 'channel'],
                condition=Q(employer=None, owner=None),
                name='unique_recipient_job_channel'
            ),
        ]

class Article(AuditFields):
    source = models.CharField(max_length=40)
    url = models.URLField()
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)
    professions = models.ManyToManyField(Taxonomy, related_name='profession_articles')
    industries = models.ManyToManyField(Taxonomy, related_name='industry_articles')
    companies = models.JSONField()
