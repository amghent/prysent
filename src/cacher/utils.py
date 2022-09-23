import os

from django.conf import settings
from django.utils.timezone import now

from cacher.models import Cache
from scheduler.models import Schedule


class Utils:
    @classmethod
    def clean_cache(cls):
        # Delete all files in the HTML dir
        for file in os.listdir(settings.HTML_DIR):
            path = os.path.join(settings.HTML_DIR, file)
            if os.path.exists(path):
                os.remove(path)

        # Delete all objects from the cache table
        Cache.objects.all().delete()

        # Update all records in the scheduler, so they are regenerated on the next pass of the scheduler
        scheduler = Schedule.objects.all()

        for schedule in scheduler:
            schedule.next_run = now()

        Schedule.objects.bulk_update(scheduler, fields=["next_run"])
