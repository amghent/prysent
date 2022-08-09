import django.db.models
from django.db import models
from django.db.models import Model

from access.models import OrganizationalUnit


class Dashboard(Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    slug = models.CharField(max_length=15, null=False, blank=False)
    menu = models.CharField(max_length=25, null=False, blank=False)

    owner = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.slug}"
