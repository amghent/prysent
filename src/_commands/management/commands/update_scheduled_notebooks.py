from django.core.management.base import BaseCommand

from scheduler.utils import Utils as SchedulerUtils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        SchedulerUtils.update_scheduled_notebooks()
