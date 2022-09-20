import os

import pandas
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Max

from _world_api.models import City
from dashboard.models import OrganizationalUnit, Dashboard, Link1, DataPage, Cardbox, CardboxType, Block1, Block2, \
    Link2, Link3


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.__flag_start_sync()

        try:
            ou_public = OrganizationalUnit.objects.get(slug="public")
        except OrganizationalUnit.DoesNotExist:
            ou_public = OrganizationalUnit()

            ou_public.slug = "public"
            ou_public.name = "public"

            ou_public.save()

            print("Created: public organizational unit")

            cardbox_type = CardboxType()

            cardbox_type.slug = "none"
            cardbox_type.width = 12

            cardbox_type.save()

            print("Created: cardbox type 'none'")
            print("Creating: cities")

            rows = self.__read_csv("world_cities.csv", 0)

            for row in rows:
                c = City()

                c.name, c.name_ascii, c.lat, c.lng, c.country, c.iso2, c.iso3, c.admin_name, c.capital, \
                    c.population, c.id = tuple(row)

                if c.iso2 == "BE":
                    c.save()

            print("Created: cities")

        media_folder = settings.MEDIA_DIR
        print(f"Media folder: { media_folder }")

        accepted_extensions = [".ipynb"]

        for dashboard_entry in os.listdir(media_folder):
            if os.path.isdir(os.path.join(media_folder, dashboard_entry)):
                dashboard = self.__handle_dashboard(dashboard_entry, ou_public)

                if dashboard is None:  # __prysent will return None of the above call
                    continue

                for level_1_entry in os.listdir(os.path.join(media_folder, dashboard_entry)):
                    if not os.path.isdir(os.path.join(media_folder, dashboard_entry, level_1_entry)):
                        self.__handle_level_1_link(level_1_entry, dashboard, accepted_extensions)
                    else:
                        menu_1 = self.__handle_level_1_block(level_1_entry, dashboard)

                        for level_2_entry in os.listdir(os.path.join(media_folder, dashboard_entry, level_1_entry)):
                            if not os.path.isdir(os.path.join(media_folder, dashboard_entry, level_1_entry,
                                                              level_2_entry)):
                                self.__handle_level_2_link(level_2_entry, menu_1, dashboard, accepted_extensions)
                            else:
                                menu_2 = self.__handle_level_2_block(level_2_entry, menu_1)

                                for level_3_entry in os.listdir(os.path.join(media_folder, dashboard_entry,
                                                                             level_1_entry, level_2_entry)):
                                    self.__handle_level_3_link(level_3_entry, menu_2, menu_1, dashboard,
                                                               accepted_extensions)

        print("Media uploaded")

        print("Database cleanup")
        self.__delete_unflagged()
        print("Database cleaned")

    @staticmethod
    def __flag_start_sync():
        Dashboard.objects.all().update(sync_flag=False)
        Block1.objects.all().update(sync_flag=False)
        Block2.objects.all().update(sync_flag=False)
        Link1.objects.all().update(sync_flag=False)
        Link2.objects.all().update(sync_flag=False)
        Link3.objects.all().update(sync_flag=False)

    @staticmethod
    def __delete_unflagged():
        Link3.objects.filter(sync_flag=False).delete()
        Link2.objects.filter(sync_flag=False).delete()
        Link1.objects.filter(sync_flag=False).delete()
        Block2.objects.filter(sync_flag=False).delete()
        Block1.objects.filter(sync_flag=False).delete()
        Dashboard.objects.filter(sync_flag=False).delete()
        # DataPages are deleted from the deletion of the links
        # Cardboxes are deleted through cascading from DataPages

    @staticmethod
    def __handle_dashboard(dashboard_entry, ou):
        slug = dashboard_entry.strip().lower().replace(" ", "_")
        menu = dashboard_entry

        if slug == "__prysent":
            return

        try:
            dashboard = Dashboard.objects.get(slug=slug)

            dashboard.sync_flag = True
            dashboard.save()

            print(f"Dashboard exists: {slug}")

        except Dashboard.DoesNotExist:
            print(f"Creating dashboard: {slug}")

            max_order = Dashboard.objects.all().aggregate(Max("order")).get("order__max")

            if max_order is None:
                max_order = 1
            else:
                max_order += 1

            dashboard = Dashboard()

            dashboard.slug = slug
            dashboard.name = menu
            dashboard.menu = menu
            dashboard.owner = ou
            dashboard.order = max_order
            dashboard.sync_flag = True
            dashboard.save()

            print(f"Created dashboard: {dashboard.slug}")

        return dashboard

    @staticmethod
    def __create_data_page(slug):
        print(f"Creating datapage: {slug}")

        data_page = DataPage()

        data_page.slug = slug
        data_page.title = ""

        data_page.save()

        print(f"Created datapage: {slug}")

        return data_page

    @staticmethod
    def __create_cardbox(data_page, notebook_path):
        print(f"Creating cardbox: {notebook_path}")

        cardbox = Cardbox()

        cardbox.data_page = data_page
        cardbox.row = 1
        cardbox.order = 1
        cardbox.type = CardboxType.objects.get(slug="none")
        cardbox.title = ""
        cardbox.height = "var(--notebook-height)"
        cardbox.notebook = notebook_path.replace("\\", "/")
        # The path is a URL for the browser, also on Windows where the path.join gives backslashes in the path
        cardbox.scroll = True

        cardbox.save()

        print(f"Created cardbox: {notebook_path}")

        return cardbox

    @staticmethod
    def __create_menu_text(menu_raw_text):
        return menu_raw_text.replace("_", " ").title()

    def __handle_common_link(self, long_slug, path_slug):
        data_page = self.__create_data_page(long_slug)
        _ = self.__create_cardbox(data_page, path_slug)

        return data_page

    def __handle_level_1_link(self, notebook, dashboard, allowed_extensions):
        slug, extension = os.path.splitext(notebook)

        if extension not in allowed_extensions:
            return None

        slug = slug.replace(" ", "_").replace("-", "_").lower()
        long_slug = f"{dashboard.slug}_{slug}"
        path_slug = os.path.join(dashboard.name, notebook)
        menu = self.__create_menu_text(slug)

        try:
            link = Link1.objects.get(dashboard_id=dashboard.id, slug=slug)

            link.sync_flag = True
            link.save()

            print(f"Link exists: {path_slug}")

        except Link1.DoesNotExist:
            print(f"Creating link: {path_slug}")

            data_page = self.__handle_common_link(long_slug, path_slug)
            max_order = Link1.objects.filter(dashboard_id=dashboard.id).aggregate(Max("order")).get("order__max")

            if max_order is None:
                max_order = 1
            else:
                max_order += 1

            link = Link1()
            link.dashboard, link.order, link.slug, link.menu, link.data_page, link.sync_flag = \
                dashboard, max_order, slug, menu, data_page, True
            link.save()

            print(f"Created link: {path_slug}")

        return link

    def __handle_level_2_link(self, notebook, menu1, dashboard, allowed_extensions):
        slug, extension = os.path.splitext(notebook)

        if extension not in allowed_extensions:
            return None

        slug = slug.replace(" ", "_").replace("-", "_").lower()
        long_slug = f"{dashboard.slug}_{menu1.slug}_{slug}"
        path_slug = os.path.join(dashboard.name, menu1.name, notebook)
        menu = self.__create_menu_text(slug)

        try:
            link = Link2.objects.get(block1=menu1, slug=slug)

            link.sync_flag = True
            link.save()

            print(f"Link exists: {path_slug}")

        except Link2.DoesNotExist:
            data_page = self.__handle_common_link(long_slug, path_slug)
            max_order = Link2.objects.filter(block1=menu1).aggregate(Max("order")).get("order__max")

            if max_order is None:
                max_order = 1
            else:
                max_order += 1

            print(f"Creating link: {path_slug}")

            link = Link2()
            link.data_page, link.slug, link.menu, link.order, link.sync_flag = data_page, slug, menu, max_order, True
            link.block1 = Block1.objects.get(dashboard=dashboard, slug=menu1.slug)
            link.save()

            print(f"Created link: {path_slug}")

        return link

    def __handle_level_3_link(self, notebook, menu2, menu1, dashboard, allowed_extensions):
        slug, extension = os.path.splitext(notebook)

        if extension not in allowed_extensions:
            return None

        slug = slug.replace(" ", "_").replace("-", "_").lower()
        long_slug = f"{dashboard.slug}_{menu1.slug}_{menu2.slug}_{slug}"
        path_slug = os.path.join(dashboard.name, menu1.name, menu2.name, notebook)
        menu = self.__create_menu_text(slug)

        try:
            link = Link3.objects.get(block2=menu2, slug=slug)

            link.sync_flag = True
            link.save()

            print(f"Link exists: {path_slug}")

        except Link3.DoesNotExist:
            data_page = self.__handle_common_link(long_slug, path_slug)
            max_order = Link3.objects.filter(block2=menu2).aggregate(Max("order")).get("order__max")

            if max_order is None:
                max_order = 1
            else:
                max_order += 1

            print(f"Creating link: {path_slug}")

            link = Link3()
            link.slug, link.menu, link.data_page, link.order, link.sync_flag = slug, menu, data_page, max_order, True
            link.block2 = Block2.objects.get(block1=menu1, slug=menu2.slug)
            link.save()

            print(f"Created link: {path_slug}")

        return link

    @staticmethod
    def __handle_level_1_block(block_entry, dashboard):
        slug = block_entry.replace(" ", "_").replace("-", "_").lower()

        try:
            block = Block1.objects.get(dashboard=dashboard, slug=slug)

            block.sync_flag = True
            block.save()

            print(f"Block exists: {os.path.join(dashboard.name, block_entry)} ")

        except Block1.DoesNotExist:
            print(f"Creating block: {os.path.join(dashboard.name, block_entry)}")

            max_order = Block1.objects.filter(dashboard=dashboard).aggregate(Max("order")).get("order__max")

            if max_order is None:
                max_order = 1
            else:
                max_order += 1

            block = Block1()

            block.slug = slug
            block.menu = block_entry.replace("_", " ").replace("-", " ").title()
            block.name = block_entry
            block.order = max_order
            block.dashboard = dashboard
            block.sync_flag = True

            block.save()

            print(f"Created block: {os.path.join(dashboard.name, block_entry)}")

        return block

    @staticmethod
    def __handle_level_2_block(block_entry, menu):
        slug = block_entry.replace(" ", "_").replace("-", "_").lower()

        try:
            block = Block2.objects.get(block1=menu, slug=slug)

            block.sync_flag = True
            block.save()

            print(f"Block exists: {os.path.join(menu.dashboard.name, menu.name, block_entry)}")

        except Block2.DoesNotExist:
            print(f"Creating block: {os.path.join(menu.dashboard.name, menu.name, block_entry)}")

            max_order = Block2.objects.filter(block1=menu).aggregate(Max("order")).get("order__max")

            if max_order is None:
                max_order = 1
            else:
                max_order += 1

            block = Block2()

            block.slug = slug
            block.menu = block_entry.replace("_", " ").replace("-", " ").title()
            block.name = block_entry
            block.order = max_order
            block.block1 = menu
            block.sync_flag = True

            block.save()

            print(f"Created block {os.path.join(menu.dashboard.name, menu.name, block_entry)}")

        return block

    @staticmethod
    def __read_csv(file_name, filler):
        print(f"Reading {file_name}")

        file = os.path.join(os.getcwd(), "src", "utils", "management", "presets", file_name)
        data = pandas.read_csv(file)
        data = data.fillna(filler)

        rows = []

        for _, r in data.iterrows():
            rows.append(r)

        return rows