from django.core.management.base import BaseCommand

from _samples.utils import Utils as SamplesUtils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        SamplesUtils.upload()
        SamplesUtils.upload_world_cities()
