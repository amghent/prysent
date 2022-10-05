from django.core.management.base import BaseCommand

import configurator.utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        configurator.utils.Utils.upload_settings()
