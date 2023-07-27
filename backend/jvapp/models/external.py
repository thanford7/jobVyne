__all__ = ['ExternalCompanyData']
from django.db import models


class ExternalCompanyData(models.Model):
    company_name = models.CharField(max_length=100, unique=True)
    linkedin_handle = models.CharField(max_length=30, null=True, blank=True)
    website = models.CharField(max_length=100, unique=True, null=True, blank=True)
    industry = models.CharField(max_length=50, null=True, blank=True)
    size_min = models.SmallIntegerField(null=True, blank=True)
    size_max = models.SmallIntegerField(null=True, blank=True)
    company_type = models.CharField(max_length=20, null=True, blank=True)
    founded_year = models.SmallIntegerField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
