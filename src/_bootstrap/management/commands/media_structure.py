import os
import shutil

import yaml as yaml

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from dashboard.models import Dashboard


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        media_folder = os.path.abspath(os.path.join(settings.BASE_DIR, "..", "..", "media"))
        print(f"Media folder: { media_folder }")

        if not(os.path.exists(media_folder)):
            print(f"Making {media_folder}")

            os.mkdir(media_folder)

        internal_folder = os.path.join(media_folder, "__prysent")

        if not(os.path.exists(internal_folder)):
            os.mkdir(internal_folder)

        notebooks_folder = os.path.abspath(os.path.join(settings.BASE_DIR, "..", "_templates", "default", "notebooks"))

        for nb in os.listdir(notebooks_folder):
            dest_file = os.path.join(internal_folder, nb)

            if not os.path.exists(dest_file):
                src_file = os.path.join(notebooks_folder, nb)
                print(f"Coppying {src_file}")
                shutil.copy(src_file, dest_file)

        for d in Dashboard.objects.all():
            df = os.path.join(media_folder, d.slug)

            if not os.path.exists(df):
                print(f"Creating dashboard folder {df}")
                os.mkdir(df)

        print("structure created")
