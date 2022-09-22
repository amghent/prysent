import os

import pandas
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from _world_api.models import City
from dashboard.models import Dashboard, OrganizationalUnit, CardboxType, DataPage, Cardbox, Link1, Link2, Link3
from dashboard.models import Block1, Block2


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.__upload_users()
        self.__upload_ou()  # depends on users
        self.__upload_dashboards()  # depends on ou
        self.__upload_data_pages()
        self.__upload_links_1()  # depends on dashboards and data_pages
        self.__upload_blocks_1()  # depends on dashboards
        self.__upload_links_2()  # depends on blocks_1 and data_pages
        self.__upload_blocks_2()  # depends on blocks1_1
        self.__upload_links_3()  # depends on blocks_2 and data_pages
        self.__upload_cardbox_types()
        self.__upload_cardboxes()  # depends on cardbox_types and data_pages

        self.__upload_world_cities()

    @staticmethod
    def __upload_cardbox_types():
        for t in [
            {"s": "none", "w": 12},
            {"s": "extra", "w": 12},
            {"s": "large", "w": 8},
            {"s": "medium", "w": 6},
            {"s": "small", "w": 4},
            {"s": "tiny", "w": 3}
        ]:
            cardbox_type = CardboxType()

            cardbox_type.slug = t["s"]
            cardbox_type.width = t["w"]

            cardbox_type.save()

    @staticmethod
    def __read_csv(file_name, filler):
        print(f"Reading {file_name}")

        file = os.path.join(os.getcwd(), "src", "_bootstrap", "management", "presets", file_name)
        data = pandas.read_csv(file)
        data = data.fillna(filler)

        rows = []

        for _, r in data.iterrows():
            rows.append(r)

        return rows

    def __upload_users(self):
        rows = self.__read_csv("users.csv", "")

        for row in rows:
            u = User()

            u.username, u.first_name, u.last_name, u.email = tuple(row)
            u.set_password("password")
            # Must use set_password to pass unencrypted pwd, not user.password=xyz

            u.save()

    def __upload_ou(self):
        rows = self.__read_csv("ou.csv", "")

        for row in rows:
            u = OrganizationalUnit()

            u.name, u.slug, members = tuple(row)

            u.save()

            for member in members.split(";"):
                m = User.objects.get(username=member)
                u.members.add(m)

    def __upload_dashboards(self):
        rows = self.__read_csv("dashboards.csv", "")

        for row in rows:
            d = Dashboard()

            d.name, d.slug, d.menu, ou, d.order = tuple(row)
            d.owner = OrganizationalUnit.objects.get(slug=ou)

            d.save()

    def __upload_data_pages(self):
        rows = self.__read_csv("data_pages.csv", "")

        for row in rows:
            p = DataPage()

            p.slug, p.title = tuple(row)

            p.save()

    def __upload_links_1(self):
        rows = self.__read_csv("links_1.csv", "")

        for row in rows:
            i = Link1()

            i.slug, i.menu, dashboard, data, i.order = tuple(row)
            i.dashboard = Dashboard.objects.get(slug=dashboard)
            i.data_page = DataPage.objects.get(slug=data)

            i.save()

    def __upload_blocks_1(self):
        rows = self.__read_csv("blocks_1.csv", "")

        for row in rows:
            b = Block1()

            b.slug, b.menu, db, b.order = tuple(row)
            b.dashboard = Dashboard.objects.get(slug=db)

            b.save()

    def __upload_links_2(self):
        rows = self.__read_csv("links_2.csv", "")

        for row in rows:
            i = Link2()

            i.slug, i.menu, block, data, i.order = tuple(row)
            i.block1 = Block1.objects.get(slug=block)
            i.data_page = DataPage.objects.get(slug=data)

            i.save()

    def __upload_blocks_2(self):
        rows = self.__read_csv("blocks_2.csv", "")

        for row in rows:
            b = Block2()

            b.slug, b.menu, block, b.order = tuple(row)
            b.block1 = Block1.objects.get(slug=block)

            b.save()

    def __upload_links_3(self):
        rows = self.__read_csv("links_3.csv", "")

        for row in rows:
            i = Link3()

            i.slug, i.menu, block, data, i.order = tuple(row)
            i.block2 = Block2.objects.get(slug=block)
            i.data_page = DataPage.objects.get(slug=data)

            i.save()

    def __upload_cardboxes(self):
        rows = self.__read_csv("cardboxes.csv", "")

        for row in rows:
            c = Cardbox()

            c.row, c.order, cb_type, c.height, c.title, c.icon, c.notebook, data = tuple(row)
            c.type = CardboxType.objects.get(slug=cb_type)
            c.data_page = DataPage.objects.get(slug=data)

            c.save()

    def __upload_world_cities(self):
        rows = self.__read_csv("world_cities.csv", 0)

        for row in rows:
            c = City()

            c.name, c.name_ascii, c.lat, c.lng, c.country, c.iso2, c.iso3, c.admin_name, \
                c.capital, c.population, c.id = tuple(row)

            if c.iso2 == "BE":
                c.save()
