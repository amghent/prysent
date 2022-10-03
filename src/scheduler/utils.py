import logging
import os
import uuid

from datetime import datetime
from croniter import croniter

from django.conf import settings
from django.db.models import Min
from django.utils.timezone import now

import prysent.utils
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
        else:
            cls.logger.info("All notebooks are up-to-date")

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

            cls.logger.info(f"Updating notebook: {notebook_file[len(settings.MEDIA_DIR)+1:]}")

            if not os.path.exists(notebook_file):  # Cleaning up stale jobs
                cls.logger.warning(f"Found orphaned job: {notebook_file[len(settings.MEDIA_DIR)+1:]}")
                job.delete()
                continue

            # Getting the old file name before it's overwritten
            old_html_file = job.html_file

            # Deleting old file (removing stale cache, sort of)
            # Done after we have inserted the new file
            if old_html_file is not None:
                old_html_path = os.path.join(settings.MEDIA_DIR, old_html_file)

                if os.path.exists(old_html_path):
                    cls.logger.info(f"Removing old cached file: {old_html_path[len(settings.MEDIA_DIR)+1:]}")
                    os.remove(old_html_file)

            if job.html_file is None:
                job.html_file = f"{uuid.uuid4()}.html"

            job.next_run = prysent.utils.Utils.croniter_to_utc("Europe/Brussels", job.cron, timestamp)
            job.generated = False

            job.save()

            notebook = Notebook(notebook_file, job.html_file)
            notebook.convert()

            cls.logger.info(f"Done, next run at: {job.next_run}")
