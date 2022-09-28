import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from configurator.utils import Utils as ConfiguratorUtils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        logger.info(f"Media folder: {settings.MEDIA_DIR}")

        ConfiguratorUtils.check_directory(settings.MEDIA_DIR)
