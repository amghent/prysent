from django.core.management.base import BaseCommand

import media.utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        media.utils.Utils.upload()
