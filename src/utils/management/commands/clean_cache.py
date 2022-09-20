import os.path
from time import sleep

from croniter import croniter
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Min
from django.utils.datetime_safe import datetime
from django.utils.timezone import now

from dashboard.models import Schedule, Cache
from dashboard.notebook import Notebook


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("Cleaning cache")

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

        print("Finished cleaning cache")

