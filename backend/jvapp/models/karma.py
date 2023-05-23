from enum import Enum

from django.core.validators import FileExtensionValidator
from django.db import models

from jvapp.models import get_user_upload_location
from jvapp.models.abstract import ALLOWED_UPLOADS_FILE, ALLOWED_UPLOADS_IMAGE, AuditFields, JobVynePermissionsMixin


class DonationOrganization(models.Model):
    name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='donation_organizations', null=True, blank=True)
    url_main = models.CharField(max_length=100, null=True, blank=True)
    url_donation = models.CharField(max_length=100, null=True, blank=True)


class UserDonationOrganization(models.Model, JobVynePermissionsMixin):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='donation_organization')
    donation_organization = models.ForeignKey('DonationOrganization', on_delete=models.CASCADE, related_name='user')
    
    class Meta:
        unique_together = ('user', 'donation_organization')
        
    def _jv_can_create(self, user):
        return user.is_admin or user.id == self.id


class UserDonation(models.Model, JobVynePermissionsMixin):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='donation')
    donate_dt = models.DateTimeField()
    donation_organization = models.ForeignKey('DonationOrganization', on_delete=models.PROTECT, related_name='user_donation')
    donation_amount = models.FloatField()
    donation_amount_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, to_field='name', default='USD')
    donation_receipt = models.FileField(
        upload_to=get_user_upload_location,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_UPLOADS_FILE + ALLOWED_UPLOADS_IMAGE)],
        null=True, blank=True
    )
    is_verified = models.BooleanField(default=False)
    donation_reason = models.CharField(max_length=200, null=True, blank=True)
    
    def _jv_can_create(self, user):
        return user.is_admin or user.id == self.id
    
    
class UserRequest(AuditFields, JobVynePermissionsMixin):
    class RequestType(Enum):
        INTRODUCTION = 'introduction'
    
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='request')
    request_type = models.CharField(max_length=25)  # RequestType
    request_cfg = models.JSONField()
    