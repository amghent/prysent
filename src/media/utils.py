import logging
import os
from os.path import splitext

from scheduler.utils import Utils as Scheduler


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
                Scheduler.upload_config(config_path, path)
