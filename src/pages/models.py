from django.db import models
from django.db.models import Model


class Page(Model):
    slug = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=250, null=False, blank=False)

    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.title} ({self.slug})"
