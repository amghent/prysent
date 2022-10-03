import logging
import os
from datetime import datetime

import pytz
import yaml as yaml
from croniter import croniter

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def create_superuser(cls):
        cls.logger.info("Creating superuser")

        if User.objects.exists():
            cls.logger.warning("Superuser already exists")
            return

        config_folder = os.path.join(settings.COMMANDS_DIR, "management", "config", "django")
        admin_yaml_file_name = os.path.join(config_folder, "admin.yaml")
        cls.logger.debug(f"admin config file: {admin_yaml_file_name}")

        admin_pwd_yaml_file_name = os.path.join(config_folder, "admin_pwd.secret")
        cls.logger.debug(f"admin password file: {admin_pwd_yaml_file_name}")

        with open(admin_yaml_file_name, "r") as file:
            admin_yaml = yaml.load(file, Loader=yaml.FullLoader)

        with open(admin_pwd_yaml_file_name, "r") as file:
            admin_pwd_yaml = yaml.load(file, Loader=yaml.FullLoader)

        username = admin_yaml["user"]
        email = admin_yaml["email"]
        password = admin_pwd_yaml["password"]

        cls.logger.debug(f"Creating the entry in Django")
        User.objects.create_superuser(username=username, password=password, email=email)

        cls.logger.info("Created superuser")

    @classmethod
    def croniter_to_utc(cls, timezone_name: str, cron: str, timestamp: datetime = now()):
        tz = pytz.timezone(timezone_name)
        next_run = str(croniter(cron, timestamp).get_next(ret_type=datetime))[:19]
        next_run = datetime.strptime(next_run, "%Y-%m-%d %H:%M:%S")
        next_run = tz.localize(next_run, is_dst=None)
        next_run = next_run.astimezone(pytz.utc)

        return next_run
