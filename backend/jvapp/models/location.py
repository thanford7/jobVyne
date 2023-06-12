from enum import IntEnum

from django.contrib.gis.geos import Point
from django.db import models
from django.contrib.gis.db import models as spatial_models


__all__ = ('REMOTE_TYPES', 'Country', 'State', 'City', 'Location')

from django.db.models import Lookup

from jvapp.utils.data import coerce_float


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


class SridGeometryField(spatial_models.GeometryField):
    def get_db_prep_save(self, value, connection):
        # MySQL 8 can use SRIDs but Django doesn't know. Hack to get around that.
        connection.features.has_spatialrefsys_table = True
        return super().get_db_prep_save(value, connection)


class WithinMiles(Lookup):
    lookup_name = 'within_miles'

    def __init__(self, lhs, rhs):
        rhs, self.miles = rhs
        super().__init__(lhs, rhs)

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params
        point = rhs_params[0]
        return (
            "st_distance(%s, st_geomfromtext('%s', %s), 'statute mile') < %s" % (lhs, point.wkt, point.srid, self.miles),
            params
        )

SridGeometryField.register_lookup(WithinMiles)
SRID = 4326


class Location(models.Model):
    text = models.CharField(max_length=200, null=True, blank=True)  # Raw text
    is_remote = models.BooleanField(null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    latitude = models.CharField(max_length=15, null=True, blank=True)
    longitude = models.CharField(max_length=15, null=True, blank=True)
    geometry = SridGeometryField(null=True, srid=SRID)
    
    class Meta:
        unique_together = ('is_remote', 'city', 'state', 'country')
    
    def __str__(self):
        return self.text
    
    @classmethod
    def get_geometry_point(cls, latitude, longitude):
        if not any((latitude, longitude)):
            return None
        return Point(coerce_float(latitude), coerce_float(longitude), srid=SRID)
    

# Store results of geocoding lookup for efficiency and to avoid charges
class LocationLookup(models.Model):
    text = models.CharField(max_length=200, unique=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    raw_result = models.JSONField(null=True, blank=True)
