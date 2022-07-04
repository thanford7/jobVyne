from django.db import models


__all__ = ('Country', 'State')


class Country(models.Model):
    countryName = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.countryName


class State(models.Model):
    stateName = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.stateName
