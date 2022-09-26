import logging
import os
import yaml

from datetime import datetime
from croniter import croniter

from django.conf import settings
from django.db.models import Min
from django.utils.timezone import now

from cacher.utils import Utils as CacherUtils
from configurator.utils import Utils as ConfiguratorUtils

from dashboard.notebook import Notebook
from scheduler.models import Schedule


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def upload_config(cls, config_path, notebook_path):
        cls.logger.info(f"Uploading config: {config_path}")
        media_path = settings.MEDIA_DIR
        stripped_path = notebook_path[len(media_path)+1:]
        stripped_path = stripped_path.replace("\\", "/")

        with open(config_path, 'r') as config_file:
            config_yaml = yaml.safe_load(config_file)

        cron = config_yaml["cron"]
        exists = (Schedule.objects.filter(notebook=stripped_path).count() > 0)

        if exists:
            cls.logger.debug(f"Config exists, updating: {config_path}")

            schedule = Schedule.objects.get(notebook=stripped_path)

            if schedule.cron != cron or schedule.next_run is None:
                schedule.next_run = croniter(cron, now()).get_next(ret_type=datetime)
                schedule.cron = cron

                schedule.save()

            cls.logger.debug(f"Updated: {config_path}")

        else:
            cls.logger.debug(f"New config, inserting: {config_path}")

            schedule = Schedule()

            schedule.notebook = stripped_path
            schedule.next_run = croniter(cron, now()).get_next(ret_type=datetime)
            schedule.cron = cron

            schedule.save()

            cls.logger.debug(f"Inserted: {config_path}")

        cls.logger.debug(f"Uploaded config: {config_path}")

    @classmethod
    def update_notebooks(cls):
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

        CacherUtils.clean_cache()

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
