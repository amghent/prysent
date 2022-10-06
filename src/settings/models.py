from django.db import models
from django.db.models import Model


class Setting(Model):
    key = models.CharField(max_length=100, null=False, blank=False)
    value = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return f"{self.key}={self.value}"

    class Meta:
        verbose_name_plural = "Settings"

        constraints = [
            models.UniqueConstraint(fields=['key'], name='ux_settings_key'),
        ]
