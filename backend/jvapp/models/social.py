__all__ = ('SocialPlatform', 'SocialLink')
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q, UniqueConstraint

from jvapp.models.abstract import AuditFields, JobVynePermissionsMixin
from jvapp.models.employer import Employer


class SocialPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='logos', null=True, blank=True)
    is_displayed = models.BooleanField(default=True)
    sort_order = models.SmallIntegerField(default=1)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('sort_order', )
        

class SocialLink(AuditFields, JobVynePermissionsMixin):
    # Make ID random so people can't randomly guess a unique filter link
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # The default social link filter is used to auto-populate forms
    is_default = models.BooleanField(default=False, blank=True)
    is_archived = models.BooleanField(default=False, blank=True)
    name = models.CharField(max_length=250, default='General')
    # If no owner, this is an employer owned link
    # If owner and employer, this is an employee referral link
    owner = models.ForeignKey('JobVyneUser', on_delete=models.CASCADE, null=True, blank=True)
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE, null=True, blank=True)
    job_subscriptions = models.ManyToManyField('JobSubscription')
    
    class Meta:
        ordering = ('-is_default', '-modified_dt')
        constraints = [
            UniqueConstraint(
                fields=['employer', 'owner'],
                condition=Q(owner__isnull=False, employer__isnull=False),
                name='unique_employer_owner'
            ),
            UniqueConstraint(
                fields=['is_default', 'owner'],
                condition=Q(owner__isnull=False, employer__isnull=True, is_default=True),
                name='unique_owner_default'
            ),
            UniqueConstraint(
                fields=['is_default', 'employer'],
                condition=Q(owner__isnull=True, employer__isnull=False, is_default=True),
                name='unique_employer_default'
            )
        ]
    
    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        if user.is_admin:
            return query
        
        social_link = Q(owner_id=user.id)
        if user.is_employer:
            social_link |= (Q(employer_id=user.employer_id) & Q(owner_id__isnull=True))
        
        return query.filter(social_link)
    
    def _jv_can_create(self, user):
        return any((
            user.is_admin,
            user.id == self.owner_id,
            (user.is_employer and self.employer_id == user.employer_id)
        ))
    
    @property
    def unique_key(self):
        job_subscription_ids = [js.id for js in self.job_subscriptions.all()]
        job_subscription_ids.sort()
        return self.owner_id, self.employer_id, tuple(job_subscription_ids)
    
    def get_link_url(self, platform_name=None):
        link = settings.BASE_URL
        if self.employer_id:
            if self.employer.organization_type == Employer.ORG_TYPE_EMPLOYER:
                link += '/co'
            else:
                link += '/group'
            link += f'/{self.employer.employer_key}/'
        else:
            link += '/jobs/'
        
        # Add query params
        job_subscriptions = self.job_subscriptions.all()
        if any((job_subscriptions, self.owner_id, platform_name)):
            link += '?'
            params = []
            if self.owner_id:
                params.append(f'connect={self.owner_id}')
            if platform_name:
                params.append(f'platform={platform_name}')
            for sub in job_subscriptions:
                params.append(f'sub={sub.id}')
            
            link += '&'.join(params)
        
        return link
    
    @property
    def is_employee_referral(self):
        job_subscriptions = self.job_subscriptions.all()
        if len(job_subscriptions) != 1:
            return False
        job_subscription = job_subscriptions[0]
        return bool(self.owner_id and self.employer_id and job_subscription.is_employer_subscription)
    