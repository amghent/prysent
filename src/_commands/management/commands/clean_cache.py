from django.core.management.base import BaseCommand

import cacher.utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        cacher.utils.Utils.clean_cache()
