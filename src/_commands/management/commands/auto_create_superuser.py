from django.core.management.base import BaseCommand

import prysent.utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        prysent.utils.Utils.create_superuser()
