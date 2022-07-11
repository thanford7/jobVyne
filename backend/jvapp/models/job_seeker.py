from django.core.validators import FileExtensionValidator
from django.db import models

from jvapp.models.abstract import ALLOWED_UPLOADS_FILE, AuditFields, JobVynePermissionsMixin


class JobApplicationFields(AuditFields):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    linkedin_url = models.CharField(max_length=75, null=True, blank=True)
    resume = models.FileField(
        upload_to='resumes',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_FILE)]
    )

    class Meta:
        abstract = True


class JobApplication(JobApplicationFields):
    
    social_link_filter = models.ForeignKey(
        'SocialLinkFilter', on_delete=models.SET_NULL, null=True, blank=True, related_name='job_application'
    )
    employer_job = models.ForeignKey(
        'EmployerJob', on_delete=models.CASCADE, related_name='job_application'
    )
    
    class Meta:
        unique_together = ('employer_job', 'email')


class JobApplicationTemplate(JobApplicationFields, JobVynePermissionsMixin):
    
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, unique=True)
    
    def _jv_can_create(self, user):
        return self.owner_id == user.id
    