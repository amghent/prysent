import logging

from time import sleep

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from configurator.utils import Utils as ConfiguratorUtils
from scheduler.utils import Utils as SchedulerUtils


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        logger.info("Starting scheduler")

        ConfiguratorUtils.create_basic_dirs()

        last_second = -1  # Instead of checking on 0, I check on the change of minute

        while True:
            timestamp = now()
            logger.debug(timestamp)

            if timestamp.second < last_second:
                logger.info(f"Verifying at {timestamp}")

                SchedulerUtils.update_scheduled_notebooks()
                SchedulerUtils.remove_cached_notebooks()

            last_second = timestamp.second
            sleep(1)
