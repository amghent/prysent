import os
import yaml as yaml

from django.conf import settings
from django.contrib.auth.models import User


class Utils:
    @classmethod
    def create_superuser(cls):
        if User.objects.exists():
            print("superuser already exists")
            return

        config_folder = os.path.join(settings.BASE_DIR.parent, "utils", "management", "config", "django")
        admin_yaml_file_name = os.path.join(config_folder, "admin.yaml")
        admin_pwd_yaml_file_name = os.path.join(config_folder, "admin_pwd.secret")

        with open(admin_yaml_file_name, "r") as file:
            admin_yaml = yaml.load(file, Loader=yaml.FullLoader)

        with open(admin_pwd_yaml_file_name, "r") as file:
            admin_pwd_yaml = yaml.load(file, Loader=yaml.FullLoader)

        username = admin_yaml["user"]
        email = admin_yaml["email"]
        password = admin_pwd_yaml["password"]

        User.objects.create_superuser(username=username, password=password, email=email)

        print("superuser created")
