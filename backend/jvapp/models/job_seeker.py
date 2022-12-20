from enum import Enum

from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q

from jvapp.models.user import PermissionName, get_user_upload_location
from jvapp.models.abstract import ALLOWED_UPLOADS_FILE, AuditFields, JobVynePermissionsMixin

__all__ = ('JobApplication', 'JobApplicationTemplate')


class JobApplicationFields(AuditFields):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    linkedin_url = models.CharField(max_length=75, null=True, blank=True)
    resume = models.FileField(
        upload_to=get_user_upload_location,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_FILE)]
    )

    class Meta:
        abstract = True


class JobApplication(JobApplicationFields, JobVynePermissionsMixin):
    class FeedbackKnowApplicantOpt(Enum):
        NO_KNOW = 0
        YES_KNOW_PROFESSIONALLY = 1
        YES_KNOW_SOCIALLY = 2
        
    class FeedbackRecommendOpt(Enum):
        NO = 0
        YES = 1
        NOT_SURE = 2
        NOT_APPLICABLE = 3
    
    user = models.ForeignKey('JobVyneUser', null=True, blank=True, related_name='job_application', on_delete=models.CASCADE)
    social_link_filter = models.ForeignKey(
        'SocialLinkFilter', on_delete=models.SET_NULL, null=True, blank=True, related_name='job_application'
    )
    platform = models.ForeignKey('SocialPlatform', on_delete=models.SET_NULL, null=True, blank=True)
    employer_job = models.ForeignKey(
        'EmployerJob', on_delete=models.CASCADE, related_name='job_application'
    )
    
    # Delivery notifications
    notification_email_dt = models.DateTimeField(null=True, blank=True)
    notification_email_failure_dt = models.DateTimeField(null=True, blank=True)
    notification_ats_dt = models.DateTimeField(null=True, blank=True)
    notification_ats_failure_dt = models.DateTimeField(null=True, blank=True)
    notification_ats_failure_msg = models.CharField(max_length=1000, null=True, blank=True)
    
    # Referrer feedback
    feedback_know_applicant = models.SmallIntegerField(null=True, blank=True)
    feedback_recommend_any_job = models.SmallIntegerField(null=True, blank=True)
    feedback_recommend_this_job = models.SmallIntegerField(null=True, blank=True)
    feedback_note = models.TextField(null=True, blank=True)
    
    #  Referral bonus tracking
    referral_bonus = models.FloatField(default=0)
    referral_bonus_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, to_field='name', default='USD')
    referral_bonus_details = models.JSONField()
    
    ats_application_key = models.CharField(max_length=30, null=True, blank=True)
    
    class Meta:
        unique_together = ('employer_job', 'email')
        
    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        applier_filter = Q(user_id=user.id)
        if user.is_email_verified:
            applier_filter |= Q(email=user.email)
            
        employer_filter = Q(employer_job__employer_id=user.employer_id)
        referrer_filter = Q(social_link_filter__owner_id=user.id)
        filter = applier_filter | referrer_filter
        if user.is_employer:
            filter |= employer_filter

        return query.filter(filter)


class JobApplicationTemplate(JobApplicationFields, JobVynePermissionsMixin):
    
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, unique=True, related_name='application_template')
    
    def _jv_can_create(self, user):
        return self.owner_id == user.id
    