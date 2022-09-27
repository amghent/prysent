from django.db import models
from django.db.models import Model


class Schedule(Model):
    notebook = models.CharField(max_length=1024, null=False, blank=False)
    cron = models.CharField(max_length=50, null=False, blank=False)
    next_run = models.DateTimeField(null=True, default=None)
    html_file = models.CharField(max_length=1024, null=True, default=None)
    generated = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name_plural = "Schedulers"

        constraints = [
            models.UniqueConstraint(fields=['notebook'], name='ux_schedule_notebook'),
        ]
