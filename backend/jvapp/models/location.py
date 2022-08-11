from django.db import models


__all__ = ('Country', 'State', 'Location')


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    
class Location(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True, unique=True)  # Raw text
    is_remote = models.BooleanField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('is_remote', 'city', 'state', 'country')
    
    def __str__(self):
        return self.text
