import logging
import os

from datetime import datetime
from croniter import croniter

from django.conf import settings
from django.db.models import Min
from django.utils.timezone import now

from cacher.models import Cache
from configurator.utils import Utils as ConfiguratorUtils

from dashboard.notebook import Notebook
from scheduler.models import Schedule


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def update_scheduled_notebooks(cls):
        ConfiguratorUtils.create_basic_dirs()

        run_jobs = False
        timestamp = now()
        next_run = Schedule.objects.aggregate(Min('next_run'))["next_run__min"]

        if next_run is not None and next_run <= now():
            # If there are expired jobs, run them
            run_jobs = True

        elif Schedule.objects.filter(html_file=None).count() > 0:
            # No expired jobs, but maybe other jobs have not yet run at all and don't have a html file available
            run_jobs = True

        if run_jobs:
            cls.__run_jobs(timestamp=timestamp)

    @classmethod
    def remove_cached_notebooks(cls):
        timestamp = now()
        stale = Cache.objects.filter(cached_until__lt=timestamp)
        page = None

        for page in stale:
            cls.logger.info(f"Removing from cache: {page.html_file}")
            cached_file = os.path.join(settings.MEDIA_DIR, page.cached_html)

            if os.path.exists(cached_file):
                os.remove(cached_file)

            page.delete()

        if page is None:
            cls.logger.info("No cache removed")

    @classmethod
    def __run_jobs(cls, timestamp):
        jobs = Schedule.objects.filter(next_run__lte=timestamp) | Schedule.objects.filter(html_file=None)

        for job in jobs:
            notebook_file = os.path.join(settings.MEDIA_DIR, job.notebook)

            cls.logger.info(f"Updating notebook: {notebook_file}")

            # Getting the old file name before it's overwritten
            old_html_file = job.html_file

            if not os.path.exists(notebook_file):  # Cleaning up stale jobs
                cls.logger.warning(f"Found orphaned job: {notebook_file}")
                job.delete()
                continue

            notebook = Notebook(notebook_file)

            job.html_file = notebook.convert()
            job.next_run = croniter(job.cron, timestamp).get_next(ret_type=datetime)

            # Deleting old file (removing stale cache, sort of)
            # Done after we have inserted the new file
            if old_html_file is not None:
                old_html_path = os.path.join(settings.MEDIA_DIR, old_html_file)

                if os.path.exists(old_html_path):
                    cls.logger.info(f"Removing old cached file: {old_html_path}")
                    os.remove(old_html_file)

            job.save()

            cls.logger.info(f"Done, next run at: {job.next_run}")
