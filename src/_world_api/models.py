from django.db import models
from django.db.models import Model


class City(Model):
    # id is added by default
    name = models.CharField(max_length=100, null=False, blank=False)
    name_ascii = models.CharField(max_length=100, null=False, blank=False)
    lat = models.FloatField(null=False)
    lng = models.FloatField(null=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    iso2 = models.CharField(max_length=2, null=False, blank=False)
    iso3 = models.CharField(max_length=3, null=False, blank=False)
    admin_name = models.CharField(max_length=100, null=False, blank=False)
    capital = models.CharField(max_length=100, null=False, blank=False)
    population = models.BigIntegerField(null=False)

    def __str__(self):
        return self.name_ascii
