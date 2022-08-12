from django.db import models

__all__ = ('Currency',)


class Currency(models.Model):
    name = models.CharField(max_length=20, unique=True)
    symbol = models.CharField(max_length=5)
