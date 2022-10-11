import logging
import os
import uuid

from time import sleep

from django.conf import settings
from django.db.models import Min
from django.utils.timezone import now

import media.utils
import prysent.utils
import configurator.utils

from cacher.models import Cache

from dashboard.notebook import Notebook
from scheduler.models import Schedule
from settings.models import Setting


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def run(cls):
        cls.logger.info("Starting scheduler")

        configurator.utils.Utils.create_basic_dirs()

        remove_cached_notebooks_cron = Setting.objects.get(key="remove_cached_notebooks_cron").value
        upload_media_cron = Setting.objects.get(key="upload_media_cron").value
        upload_schedule_cron = Setting.objects.get(key="upload_schedule_cron").value
        upload_settings_cron = Setting.objects.get(key="upload_settings_cron").value
        update_scheduled_cron = Setting.objects.get(key="update_scheduled_notebooks_cron").value

        timestamp = now()
        timezone = Setting.objects.get(key="timezone").value
        cls.logger.info(f"timezone: {timezone}")

        last_second = -1  # Instead of checking on 0, I check on the change of minute

        remove_cached_notebooks_next = prysent.utils.Utils.croniter_to_utc(timezone, remove_cached_notebooks_cron,
                                                                           timestamp)
        upload_media_next = prysent.utils.Utils.croniter_to_utc(timezone, upload_media_cron, timestamp)
        upload_schedule_next = prysent.utils.Utils.croniter_to_utc(timezone, upload_schedule_cron, timestamp)
        upload_settings_next = prysent.utils.Utils.croniter_to_utc(timezone, upload_settings_cron, timestamp)
        update_notebooks_next = prysent.utils.Utils.croniter_to_utc(timezone, update_scheduled_cron, timestamp)

        while True:
            timestamp = now()
            cls.logger.debug(timestamp)

            if timestamp.second < last_second:
                cls.logger.info(f"Verifying at {timestamp}")

                if timestamp > upload_settings_next:
                    configurator.utils.Utils.upload_settings()
                    upload_settings_next = prysent.utils.Utils.croniter_to_utc(timezone, upload_settings_cron,
                                                                               timestamp)
                if timestamp > upload_schedule_next:
                    configurator.utils.Utils.check_directory(settings.MEDIA_DIR)
                    upload_schedule_next = prysent.utils.Utils.croniter_to_utc(timezone, upload_schedule_cron,
                                                                               timestamp)

                if timestamp > upload_media_next:
                    media.utils.Utils.upload()
                    upload_media_next = prysent.utils.Utils.croniter_to_utc(timezone, upload_media_cron, timestamp)

                if timestamp > update_notebooks_next:
                    cls.update_scheduled_notebooks()
                    update_notebooks_next = prysent.utils.Utils.croniter_to_utc(timezone, update_scheduled_cron,
                                                                                timestamp)

                if timestamp > remove_cached_notebooks_next:
                    cls.remove_cached_notebooks()
                    remove_cached_notebooks_next = prysent.utils.Utils.croniter_to_utc(timezone,
                                                                                       remove_cached_notebooks_cron,
                                                                                       timestamp)

            last_second = timestamp.second
            sleep(1)

    @classmethod
    def update_scheduled_notebooks(cls):
        configurator.utils.Utils.create_basic_dirs()

        run_jobs = False
        timestamp = now()
        next_run = Schedule.objects.aggregate(Min('next_run'))["next_run__min"]

        if next_run is not None and next_run <= now():
            # If there are expired jobs, run them
            run_jobs = True

        elif Schedule.objects.filter(cached_html=None).count() > 0:
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
            cls.logger.info(f"Removing from cache: {page.cached_html}")
            cached_file = os.path.join(settings.MEDIA_DIR, page.cached_html)

            if os.path.exists(cached_file):
                os.remove(cached_file)

            page.delete()

        if page is None:
            cls.logger.info("No cache removed")

    @classmethod
    def __run_jobs(cls, timestamp):
        jobs = Schedule.objects.filter(next_run__lte=timestamp) | Schedule.objects.filter(cached_html=None)
        timezone = Setting.objects.get(key="timezone").value

        for job in jobs:
            notebook_file = os.path.join(settings.MEDIA_DIR, job.notebook)
            internal_file = prysent.utils.Utils.filepath_to_internal(notebook_file)

            cls.logger.info(f"Updating notebook: {internal_file}")

            if not os.path.exists(notebook_file):  # Cleaning up stale jobs
                cls.logger.warning(f"Found orphaned job: {internal_file}")
                job.delete()
                continue

            # Getting the old file name before it's overwritten
            old_html_file = job.cached_html

            # Deleting old file (removing stale cache, sort of)
            # Done after we have inserted the new file
            if old_html_file is not None:
                old_html_path = os.path.join(settings.MEDIA_DIR, old_html_file)
                old_internal_file = prysent.utils.Utils.filepath_to_internal(old_html_path)

                if os.path.exists(old_html_path):
                    cls.logger.info(f"Removing old cached file: {old_internal_file}")
                    os.remove(old_html_file)

            if job.cached_html is None:
                job.cached_html = f"{uuid.uuid4()}.html"

            job.next_run = prysent.utils.Utils.croniter_to_utc(timezone, job.cron, timestamp)
            job.generated = False

            job.save()

            notebook = Notebook(notebook_file, job.cached_html)
            notebook.convert()

            cls.logger.info(f"Done, next run at: {job.next_run}")
