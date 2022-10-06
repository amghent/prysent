import logging
import os
from datetime import timedelta
from threading import Thread

from django.conf import settings
from django.utils.timezone import now

from cacher.models import Cache
from dashboard.notebook import Notebook
from scheduler.models import Schedule

from dashboard.notebook import GENERATION_STATUS_FAILED
from settings.models import Setting

CACHER_GENERATION_STARTED = "GENERATION_STARTED"
CACHER_GENERATION_TIMEOUT = "GENERATION_TIMEOUT"
CACHER_GENERATION_ERROR = "GENERATION_ERROR"
CACHER_GENERATION_ONGOING = "GENERATION_ONGOING"


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def get_cached_html(cls, path, cache_seconds=-1):
        cls.logger.info(f"Checking if cached: {path}")

        if cache_seconds < 0:
            cache_seconds = Setting.objects.get(key="cache_seconds").value

        cls.logger.debug(f"Caching seconds: {path}")

        try:
            scheduled = Schedule.objects.get(notebook=path)

            if scheduled.generation_status == GENERATION_STATUS_FAILED:
                return CACHER_GENERATION_ERROR, False, scheduled.generation_message

            if scheduled.html_file is None:
                cls.logger.warning("Schedule file is not generated yet. Starting generation")

                notebook = Notebook(path)
                Thread(target=notebook.convert).start()

                scheduled.cached_html = notebook.export_path
                scheduled.generated = False
                scheduled.generation_timeout = now() + timedelta(minutes=cache_seconds)
                scheduled.save()

                return CACHER_GENERATION_STARTED, False, ""

            else:

                if os.path.exists(os.path.join(settings.HTML_DIR, scheduled.html_file)):
                    cls.logger.info(f"Returning scheduled file: {scheduled.html_file}")

                    return scheduled.html_file, True, ""

                else:
                    if scheduled.generated is True:
                        cls.logger.warning("Schedule file does not exist anymore. Starting generation")

                        scheduled.generated = False
                        scheduled.generation_timeout = now() + timedelta(minutes=cache_seconds)
                        scheduled.save()

                        notebook = Notebook(path, scheduled.html_file)
                        Thread(target=notebook.convert).start()

                        return CACHER_GENERATION_STARTED, False, ""
                    else:
                        if scheduled.generation_timeout is not None and scheduled.generation_timeout < now():
                            cls.logger.error("Scheduled file generation has timed out")

                            return CACHER_GENERATION_TIMEOUT, False, ""

                        cls.logger.info("Scheduled file is not yet generated. Must wait a bit")

                        return CACHER_GENERATION_ONGOING, False, ""

        except Schedule.DoesNotExist:
            pass

        try:
            cached = Cache.objects.get(notebook=path)

            if cached.generation_status == GENERATION_STATUS_FAILED:
                return CACHER_GENERATION_ERROR, False, cached.generation_message

            if os.path.exists(os.path.join(settings.HTML_DIR, cached.cached_html)):
                cached.cached_until = now() + timedelta(minutes=cache_seconds)
                cached.save()

                cls.logger.info(f"returning scheduled file: {cached.cached_html}")

                return cached.cached_html, True, ""
            else:
                if cached.generated is True:
                    cls.logger.warning("Cached file does not exist anymore. Regenerating")

                    cached.generated = False
                    cached.generation_timeout = now() + timedelta(minutes=cache_seconds)
                    cached.save()

                    notebook = Notebook(path, cached.cached_html)
                    Thread(target=notebook.convert).start()

                    return CACHER_GENERATION_STARTED, False, ""

                else:
                    if cached.generation_timeout is not None and cached.generation_timeout < now():
                        cls.logger.error("Cached file generation has timeout out")

                        return CACHER_GENERATION_TIMEOUT, False, ""

                    else:
                        cls.logger.info("Cached file does not exist yet. Must wait a bit")

                        return CACHER_GENERATION_ONGOING, False, ""

        except Cache.DoesNotExist:
            cls.logger.info(f"Not cached: {path}")

            notebook = Notebook(path)
            Thread(target=notebook.convert).start()

            cache = Cache()
            cache.notebook = path
            cache.cached_until = now() + timedelta(minutes=cache_seconds)
            cache.cached_html = notebook.export_path
            cache.generated = False
            cache.generation_timeout = now() + timedelta(minutes=1)
            cache.save()

            return CACHER_GENERATION_ONGOING, False, ""

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
            schedule.cached_html = None
            schedule.generated = False
            schedule.generation_status = 0
            schedule.generation_message = None

        Schedule.objects.bulk_update(scheduler, fields=["next_run", "cached_html", "generated", "generation_status",
                                                        "generation_message"])

        cls.logger.info("Finished cleaning cache")
