from enum import IntEnum

from django.db import models


__all__ = ('REMOTE_TYPES', 'Country', 'State', 'City', 'Location')


class REMOTE_TYPES(IntEnum):
    NO = 1
    YES = 2


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    
class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    
class Location(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True, unique=True)  # Raw text
    is_remote = models.BooleanField(null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    latitude = models.CharField(max_length=15, null=True, blank=True)
    longitude = models.CharField(max_length=15, null=True, blank=True)
    
    class Meta:
        unique_together = ('is_remote', 'city', 'state', 'country')
    
    def __str__(self):
        return self.text
    

# Store results of geocoding lookup for efficiency and to avoid charges
class LocationLookup(models.Model):
    text = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    raw_result = models.JSONField()
