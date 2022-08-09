from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class OrganizationalUnit(Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.CharField(max_length=15, null=False, blank=False)

    members = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.slug}"
