from django.db import models

__all__ = ('Waitlist', 'SalesInquiry')


class Waitlist(models.Model):
    email = models.EmailField()
    created_dt = models.DateTimeField()
    
    
class SalesInquiry(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company_name = models.CharField(max_length=75)
    email = models.EmailField()
    created_dt = models.DateTimeField()
