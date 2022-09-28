from django.core.management.base import BaseCommand

from media.utils import Utils as MediaUtils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        MediaUtils.upload()
