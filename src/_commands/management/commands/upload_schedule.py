import logging

from django.conf import settings
from django.core.management.base import BaseCommand

import configurator.utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        logger.info(f"Media folder: {settings.MEDIA_DIR}")

        configurator.utils.Utils.check_directory(settings.MEDIA_DIR)
