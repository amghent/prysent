from django.core.management.base import BaseCommand
from django.db.models import Min
from django.utils.timezone import now

from cacher.utils import Utils as CacherUtils
from configurator.utils import Utils as ConfiguratorUtils
from scheduler.utils import Utils as SchedulerUtils

from scheduler.models import Schedule


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        SchedulerUtils.get_expired_jobs()

        ConfiguratorUtils.create_basic_dirs()

        run_jobs = False
        timestamp = now()
        next_run = Schedule.objects.aggregate(Min('next_run'))["next_run__min"]

        if next_run is not None and next_run <= now():
            # If there are expired jobs, run them
            run_jobs = True

        elif Schedule.objects.filter(html_file=None).count() > 0:
            # No expired jobs, but maybe other jobs have not yet run at all and don't have a html file available
            run_jobs = True

        if run_jobs:
            SchedulerUtils.run_jobs(timestamp=timestamp)

        CacherUtils.clean_cache()
