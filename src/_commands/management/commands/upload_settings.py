from django.core.management.base import BaseCommand

from configurator.utils import Utils as ConfiguratorUtils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        ConfiguratorUtils.upload_settings()
