from django.core.management.base import BaseCommand

from cacher.utils import Utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Utils.clean_cache()
