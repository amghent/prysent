import os

import pandas
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from _world_api.models import City
from access.models import OrganizationalUnit
from dashboard.models import Dashboard


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.__upload_users()
        self.__upload_ou()
        self.__upload_dashboards()
        self.__upload_world_cities()

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

    def __upload_world_cities(self):
        rows = self.__read_csv("world_cities.csv", 0)

        for row in rows:
            c = City()

            c.name, c.name_ascii, c.lat, c.lng, c.country, c.iso2, c.iso3, c.admin_name, \
                c.capital, c.population, c.id = tuple(row)

            c.save()
