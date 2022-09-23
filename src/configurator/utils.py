import os

from django.conf import settings


class Utils:
    @classmethod
    def create_basic_dirs(cls):
        if not os.path.exists(settings.HTML_DIR):
            os.mkdir(settings.HTML_DIR)
