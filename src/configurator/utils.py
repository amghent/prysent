import logging
import os
import pandas
import yaml

from os.path import splitext

from django.conf import settings
from django.utils.timezone import now

import prysent.utils

from scheduler.models import Schedule
from settings.models import Setting


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def check_media_directory(cls):
        cls.check_directory(settings.MEDIA_DIR)

    @classmethod
    def check_directory(cls, path):
        cls.logger.debug(f"Checking folder: {path}")

        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)

            if entry_path.startswith("_"):
                continue

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
        stripped_path = prysent.utils.Utils.filepath_to_internal(notebook_path)
        internal_path = prysent.utils.Utils.filepath_to_internal(config_path)

        cls.logger.info(f"Uploading config: {internal_path}")

        with open(config_path, 'r') as config_file:
            config_yaml = yaml.safe_load(config_file)

        cron = config_yaml["cron"]
        exists = (Schedule.objects.filter(notebook=stripped_path).count() > 0)

        if exists:
            cls.logger.debug(f"Config exists, updating: {internal_path}")

            schedule = Schedule.objects.get(notebook=stripped_path)

            if schedule.cron != cron or schedule.next_run is None:
                schedule.next_run = prysent.utils.Utils.croniter_to_utc("Europe/Brussels", cron)
                schedule.cron = cron
                schedule.generated = False

                schedule.save()

            cls.logger.debug(f"Updated: {internal_path}")

        else:
            cls.logger.debug(f"New config, inserting: {internal_path}")

            schedule = Schedule()

            schedule.notebook = stripped_path
            schedule.next_run = prysent.utils.Utils.croniter_to_utc("Europe/Brussels", cron)
            schedule.cron = cron
            schedule.generated = False

            schedule.save()

            cls.logger.debug(f"Inserted: {internal_path}")

        cls.logger.debug(f"now: {now()}")
        cls.logger.debug(f"next: {schedule.next_run}")

        cls.logger.debug(f"Uploaded config: {internal_path}")

    @classmethod
    def upload_settings(cls):
        config_file_path = os.path.join(settings.BASE_DIR.parent, "_commands", "management", "config", "django",
                                        "default_settings.yaml")
        internal_path = prysent.utils.Utils.filepath_to_internal(config_file_path)

        cls.logger.info(f"Reading config file {internal_path}")

        with open(config_file_path, 'r') as config_file:
            config_yaml = yaml.safe_load(config_file)

        for config in config_yaml:
            cls.logger.debug(f"Updating: {config}")

            try:
                setting = Setting.objects.get(key=config)
            except Setting.DoesNotExist:
                setting = Setting()

            setting.key = config
            setting.value = config_yaml[config]
            setting.save()

            cls.logger.debug(f"Setting value: {setting.value}")

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
