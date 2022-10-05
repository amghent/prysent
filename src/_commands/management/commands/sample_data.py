from django.core.management.base import BaseCommand

import _samples.utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        _samples.utils.Utils.upload()
        _samples.utils.Utils.upload_world_cities()
