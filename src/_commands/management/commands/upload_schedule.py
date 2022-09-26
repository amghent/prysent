import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from scheduler.utils import Utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        media_folder = settings.MEDIA_DIR
        logger.info(f"Media folder: {media_folder}")

        Utils.check_directory(media_folder)
