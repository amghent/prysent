import logging
import os

from django.conf import settings
from django.utils.timezone import now

from cacher.models import Cache
from scheduler.models import Schedule


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def clean_cache(cls):
        cls.logger.info("Cleaning cache.")

        if not os.path.exists(settings.HTML_DIR):
            cls.logger.warning(f"{settings.HTML_DIR} does not yet exist.  No cache to clean")
            return

        cls.logger.debug("Delete all files in the HTML dir")
        for file in os.listdir(settings.HTML_DIR):
            path = os.path.join(settings.HTML_DIR, file)
            cls.logger.debug(f"Removing file from cache: {path}")

            os.remove(path)

        cls.logger.debug("Delete all objects from the cache table")
        Cache.objects.all().delete()

        cls.logger.debug(
            "Update all records in the scheduler, so they are regenerated on the next pass of the scheduler")
        scheduler = Schedule.objects.all()

        for schedule in scheduler:
            schedule.next_run = now()

        Schedule.objects.bulk_update(scheduler, fields=["next_run"])

        cls.logger.info("Finished cleaning cache")
