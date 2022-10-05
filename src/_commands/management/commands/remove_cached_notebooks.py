from django.core.management.base import BaseCommand

import scheduler.utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        scheduler.utils.Utils.remove_cached_notebooks()
