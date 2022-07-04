from django.db import models


__all__ = ('AuditFields',)


class AuditFields(models.Model):
    created_dt = models.DateTimeField()
    modified_dt = models.DateTimeField()

    class Meta:
        abstract = True
