from django.core.management.base import BaseCommand

from prysent.utils import Utils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Utils.create_superuser()
