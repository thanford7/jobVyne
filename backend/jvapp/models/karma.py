import uuid
from enum import Enum

from django.core.validators import FileExtensionValidator
from django.db import models

from jvapp.models import get_user_upload_location
from jvapp.models.abstract import ALLOWED_UPLOADS_FILE, ALLOWED_UPLOADS_IMAGE, AuditFields, JobVynePermissionsMixin


class DonationOrganization(models.Model):
    ein = models.CharField(max_length=10, unique=True, null=True, blank=True)
    every_org_key = models.CharField(max_length=40, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='donation_organizations', null=True, blank=True)
    url_main = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class UserDonationOrganization(models.Model, JobVynePermissionsMixin):
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='donation_organization')
    donation_organization = models.ForeignKey('DonationOrganization', on_delete=models.CASCADE, related_name='user')
    
    class Meta:
        unique_together = ('user', 'donation_organization')

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
    
        return query.filter(user_id=user.id)
        
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

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
    
        return query.filter(user_id=user.id)
    
    def _jv_can_create(self, user):
        return user.is_admin or user.id == self.id
    
    
class UserRequest(AuditFields, JobVynePermissionsMixin):
    # Keep in sync with USER_REQUEST_TYPES frontend
    class RequestType(Enum):
        INTRODUCTION = 'introduction'
        CONNECT = 'connect'

    # Make ID random so people can't randomly guess
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, related_name='request')
    request_type = models.CharField(max_length=25)  # RequestType

    connection_first_name = models.CharField(max_length=150)
    connection_last_name = models.CharField(max_length=150, null=True, blank=True)
    connection_linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    connection_email = models.EmailField(null=True, blank=True)
    connection_phone_number = models.CharField(max_length=25, null=True, blank=True)
    connection_donation_org = models.ForeignKey('DonationOrganization', on_delete=models.SET_NULL, null=True, blank=True)
    
    connector_first_name = models.CharField(max_length=150, null=True, blank=True)
    connector_last_name = models.CharField(max_length=150, null=True, blank=True)
    connector_email = models.EmailField(null=True, blank=True)
    connector_phone_number = models.CharField(max_length=25, null=True, blank=True)
    
    request_data = models.JSONField(null=True, blank=True)

    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
    
        return query.filter(user_id=user.id)
    
    def _jv_can_create(self, user):
        return user.is_admin or user.id == self.id
    