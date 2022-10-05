from django.db import models
from django.db.models import Model


class Cache(Model):
    html_file = models.CharField(max_length=1024, null=True, default=None)
    cached_html = models.CharField(max_length=1024, null=True, default=None)
    cached_until = models.DateTimeField(null=True, default=None)
    generated = models.BooleanField(null=False, default=False)
    generation_timeout = models.DateTimeField(null=True, default=None)
    generation_status = models.IntegerField(null=False, default=0)
    generation_message = models.TextField(null=True, default=None)

    class Meta:
        verbose_name_plural = "Cached"

        constraints = [
            models.UniqueConstraint(fields=['html_file'], name='ux_cache_html_file'),
        ]
