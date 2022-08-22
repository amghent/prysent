import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from dashboard.models import Dashboard, Level1Menu, Level2Menu


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        media_folder = os.path.abspath(os.path.join(settings.BASE_DIR.parent, "media"))
        print(f"Media folder: { media_folder }")

        if not os.path.exists(media_folder):
            print(f"Making {media_folder}")

            os.mkdir(media_folder)

        internal_folder = os.path.join(media_folder, "__prysent")

        if not os.path.exists(internal_folder):
            os.mkdir(internal_folder)

        notebooks_folder = os.path.abspath(os.path.join(settings.BASE_DIR.parent, "_templates", "default", "notebooks"))

        for nb in os.listdir(notebooks_folder):
            dest_file = os.path.join(internal_folder, nb)

            if not os.path.exists(dest_file):
                src_file = os.path.join(notebooks_folder, nb)
                print(f"Copying {src_file}")
                shutil.copy(src_file, dest_file)

        for d in Dashboard.objects.all():
            df = os.path.join(media_folder, d.slug)

            if not os.path.exists(df):
                print(f"Creating dashboard folder {df}")
                os.mkdir(df)

        for m in Level1Menu.objects.all():
            d = Dashboard.objects.get(id=m.dashboard_id)
            mf = os.path.join(media_folder, d.slug, m.slug)

            if not os.path.exists(mf):
                print(f"Creating level 1 folder {mf}")
                os.mkdir(mf)

        for m in Level2Menu.objects.all():
            m1 = Level1Menu.objects.get(id=m.level1menu_id)
            d = Dashboard.objects.get(id=m1.dashboard_id)
            mf = os.path.join(media_folder, d.slug, m1.slug, m.slug)

            if not os.path.exists(mf):
                print(f"Creating level 2 folder {mf}")
                os.mkdir(mf)

        print("structure created")
