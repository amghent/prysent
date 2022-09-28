import logging
import os
from datetime import timedelta
from threading import Thread

from django.conf import settings
from django.utils.timezone import now

from cacher.models import Cache
from dashboard.notebook import Notebook
from scheduler.models import Schedule


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def get_cached_html(cls, path, cache_minutes=1):
        cls.logger.info(f"Checking if cached: {path}")

        try:
            scheduled = Schedule.objects.get(notebook=path)

            if scheduled.html_file is None:
                cls.logger.warning("Schedule file is not generated yet. Starting generation")

                notebook = Notebook(path)
                Thread(target=notebook.convert).start()

                scheduled.html_file = notebook.export_path
                scheduled.generated = False
                scheduled.save()

                return scheduled.html_file, False

            else:

                if os.path.exists(os.path.join(settings.HTML_DIR, scheduled.html_file)):
                    cls.logger.info(f"Returning scheduled file: {scheduled.html_file}")

                    return scheduled.html_file, True

                else:
                    if scheduled.generated is True:
                        cls.logger.warning("Schedule file does not exist anymore. Starting generation")

                        scheduled.generated = False
                        scheduled.save()

                        notebook = Notebook(path, scheduled.html_file)
                        Thread(target=notebook.convert).start()

                        return scheduled.html_file, False
                    else:
                        cls.logger.info("Schedule file is not yet generated. Must wait a bit")

                        return scheduled.html_file, False

        except Schedule.DoesNotExist:
            pass

        try:
            cached = Cache.objects.get(html_file=path)

            if os.path.exists(os.path.join(settings.HTML_DIR, cached.cached_html)):
                cached.cached_until = now() + timedelta(minutes=cache_minutes)
                cached.save()

                cls.logger.info(f"returning scheduled file: {cached.cached_html}")

                return cached.cached_html, True
            else:
                if cached.generated is True:
                    cls.logger.warning("Cached file does not exist anymore. Regenerating")

                    cached.generated = False
                    cached.save()

                    notebook = Notebook(path, cached.cached_html)
                    Thread(target=notebook.convert).start()
                else:
                    cls.logger.info("Cached file does not exist yet. Must wait a bit")

                return cached.cached_html, False

        except Cache.DoesNotExist:
            cls.logger.info(f"Not cached: {path}")

            notebook = Notebook(path)
            Thread(target=notebook.convert).start()

            cache = Cache()
            cache.html_file = path
            cache.cached_until = now() + timedelta(minutes=cache_minutes)
            cache.cached_html = notebook.export_path
            cache.generated = False
            cache.save()

            return notebook.export_path, False

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
