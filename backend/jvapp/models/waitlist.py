from django.db import models

__all__ = ('Waitlist', )


class Waitlist(models.Model):
    email = models.EmailField()
    created_dt = models.DateTimeField()
