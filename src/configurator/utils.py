import logging
import os
import pandas
import yaml

from datetime import datetime
from os.path import splitext
from croniter import croniter

from django.conf import settings
from django.utils.timezone import now

from scheduler.models import Schedule


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def check_directory(cls, path):
        cls.logger.debug(f"Checking folder: {path}")

        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)

            if os.path.isdir(entry_path):
                cls.check_directory(entry_path)
            else:
                cls.check_file(entry_path)

    @classmethod
    def check_file(cls, path):
        cls.logger.debug(f"Checking file: {path}")

        file, extension = splitext(path)

        if extension == ".ipynb":
            config_path = f"{file}.yaml"

            if os.path.exists(config_path) and os.path.isfile(config_path):
                cls.upload_config(config_path, path)

    @classmethod
    def upload_config(cls, config_path, notebook_path):
        media_path = settings.MEDIA_DIR
        stripped_path = notebook_path[len(media_path)+1:]
        stripped_path = stripped_path.replace("\\", "/")

        cls.logger.info(f"Uploading config: {config_path[len(media_path)+1:]}")

        with open(config_path, 'r') as config_file:
            config_yaml = yaml.safe_load(config_file)

        cron = config_yaml["cron"]
        exists = (Schedule.objects.filter(notebook=stripped_path).count() > 0)

        if exists:
            cls.logger.debug(f"Config exists, updating: {config_path[len(media_path)+1:]}")

            schedule = Schedule.objects.get(notebook=stripped_path)

            if schedule.cron != cron or schedule.next_run is None:
                schedule.next_run = croniter(cron, now()).get_next(ret_type=datetime)
                schedule.cron = cron
                schedule.generated = False

                schedule.save()

            cls.logger.debug(f"Updated: {config_path[len(media_path)+1:]}")

        else:
            cls.logger.debug(f"New config, inserting: {config_path[len(media_path)+1:]}")

            schedule = Schedule()

            schedule.notebook = stripped_path
            schedule.next_run = croniter(cron, now()).get_next(ret_type=datetime)
            schedule.cron = cron
            schedule.generated = False

            schedule.save()

            cls.logger.debug(f"Inserted: {config_path[len(media_path)+1:]}")

        cls.logger.debug(f"Uploaded config: {config_path[len(media_path)+1:]}")

    @classmethod
    def create_basic_dirs(cls):
        if not os.path.exists(settings.HTML_DIR):
            cls.logger.info(f"Creating HTML dir: {settings.HTML_DIR}")

            os.mkdir(settings.HTML_DIR)

    @classmethod
    def read_csv(cls, file_name, filler):
        cls.logger.info(f"Reading {file_name}")

        file = os.path.join(settings.BASE_DIR.parent, "_samples", "presets", file_name)
        data = pandas.read_csv(file)
        data = data.fillna(filler)

        rows = []

        for _, r in data.iterrows():
            rows.append(r)

        return rows
