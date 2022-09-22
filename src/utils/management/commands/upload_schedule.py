import os
from os.path import splitext

import yaml
from croniter import croniter
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.datetime_safe import datetime
from django.utils.timezone import now

from dashboard.models import Schedule


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        media_folder = settings.MEDIA_DIR
        print(f"Media folder: {media_folder}")

        self.__handle_dir(media_folder)

    def __handle_dir(self, path):
        print(f"Verifying directory: {path}")

        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)

            if os.path.isdir(entry_path):
                self.__handle_dir(entry_path)
            else:
                self.__handle_file(entry_path)

    @staticmethod
    def __handle_file(path):
        print(f"Verifying file: {path}")

        media_path = settings.MEDIA_DIR
        stripped_path = path[len(media_path)+1:]
        stripped_path = stripped_path.replace("\\", "/")

        file, extension = splitext(path)

        if extension == ".ipynb":
            config_path = f"{file}.yaml"

            if os.path.exists(config_path) and os.path.isfile(config_path):
                print(f"Uploading config: {config_path}")

                with open(config_path, 'r') as config_file:
                    config_yaml = yaml.safe_load(config_file)

                cron = config_yaml["cron"]
                exists = (Schedule.objects.filter(notebook=stripped_path).count() > 0)

                if exists:
                    schedule = Schedule.objects.get(notebook=stripped_path)

                    if schedule.cron != cron or schedule.next_run is None:
                        schedule.next_run = croniter(cron, now()).get_next(ret_type=datetime)
                        schedule.cron = cron

                        schedule.save()

                else:
                    schedule = Schedule()

                    schedule.notebook = stripped_path
                    schedule.next_run = croniter(cron, now()).get_next(ret_type=datetime)
                    schedule.cron = cron

                    schedule.save()
