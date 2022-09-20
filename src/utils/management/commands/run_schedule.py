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
        if not os.path.exists(settings.HTML_DIR):
            os.mkdir(settings.HTML_DIR)

        timestamp = now()

        next_run = Schedule.objects.aggregate(Min('next_run'))["next_run__min"]

        if next_run is not None and next_run <= now():
            self.__run_jobs(timestamp)

        self.__clean_cache(timestamp=timestamp)

    @staticmethod
    def __clean_cache(timestamp):
        stale = Cache.objects.filter(cached_until__lt=timestamp)
        page = None

        for page in stale:
            print(f"Removing from cache: {page.html_file}")
            cached_file = os.path.join(settings.MEDIA_DIR, page.cached_html)

            if os.path.exists(cached_file):
                os.remove(cached_file)

            page.delete()

        if page is None:
            print("No cache removed")

    @staticmethod
    def __run_jobs(timestamp):
        jobs = Schedule.objects.filter(next_run__lte=timestamp)

        for job in jobs:
            print(f"Running job: {job.notebook}")

            # Getting the old file name before it's overwritten
            old_html_file = job.html_file

            if not os.path.exists(os.path.join(settings.MEDIA_DIR, job.notebook)):  # Cleaning up stale jobs
                job.delete()
                continue

            notebook = Notebook(os.path.join(settings.MEDIA_DIR, job.notebook))

            job.html_file = notebook.convert()
            job.next_run = croniter(job.cron, timestamp).get_next(ret_type=datetime)

            # Deleting old file (removing stale cache, sort of)
            # Done after we have inserted the new file
            if old_html_file is not None and os.path.exists(old_html_file):
                os.remove(old_html_file)

            print(f"Done, next run at: {job.next_run}")

            job.save()
