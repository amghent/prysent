import os

import pandas
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from _world_api.models import City
from dashboard.models import Dashboard, OrganizationalUnit, CardboxType, NotebookPage, Cardbox, Level1Link, Level1Menu


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.__upload_users()
        self.__upload_ou()  # depends on users
        self.__upload_dashboards()  # depends on ou
        self.__upload_notebook_pages()
        self.__upload_links_1()  # depends on dashboards and notebook_pages
        self.__upload_menus_1()  # depends on dashboards
        self.__upload_cardbox_types()
        self.__upload_cardboxes()  # depends on cardbox_types and notebook_pages

        self.__upload_world_cities()

    @staticmethod
    def __upload_cardbox_types():
        for t in [
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

            d.name, d.slug, d.menu, ou = tuple(row)
            d.owner = OrganizationalUnit.objects.get(slug=ou)

            d.save()

    def __upload_notebook_pages(self):
        rows = self.__read_csv("notebook_pages.csv", "")

        for row in rows:
            p = NotebookPage()

            p.slug, p.title = tuple(row)

            p.save()

    def __upload_links_1(self):
        rows = self.__read_csv("links_1.csv", "")

        for row in rows:
            i = Level1Link()

            i.slug, i.menu, db, np = tuple(row)
            i.dashboard = Dashboard.objects.get(slug=db)
            i.notebook_page = NotebookPage.objects.get(slug=np)

            i.save()

    def __upload_menus_1(self):
        rows = self.__read_csv("menus_1.csv", "")

        for row in rows:
            m = Level1Menu()

            m.slug, m.menu, db = tuple(row)
            m.dashboard = Dashboard.objects.get(slug=db)

            m.save()

    def __upload_cardboxes(self):
        rows = self.__read_csv("cardboxes.csv", "")

        for row in rows:
            c = Cardbox()

            c.row, c.order, cb_type, c.height, c.title, c.icon, c.notebook, nb_page = tuple(row)
            c.type = CardboxType.objects.get(slug=cb_type)
            c.notebook_page = NotebookPage.objects.get(slug=nb_page)

            c.save()

    def __upload_world_cities(self):
        rows = self.__read_csv("world_cities.csv", 0)

        for row in rows:
            c = City()

            c.name, c.name_ascii, c.lat, c.lng, c.country, c.iso2, c.iso3, c.admin_name, \
                c.capital, c.population, c.id = tuple(row)

            if c.iso2 == "BE":
                c.save()
