import os

import pandas
from django.core.management.base import BaseCommand

from _world_api.models import City


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        file = os.path.join(os.getcwd(), "src", "_bootstrap", "management", "presets", "worldcities.csv")
        data = pandas.read_csv(file)
        data = data.fillna(0)

        for _, row in data.iterrows():
            c = City()

            c.name, c.name_ascii, c.lat, c.lng, c.country, c.iso2, c.iso3, c.admin_name, \
                c.capital, c.population, c.id = tuple(row)

            c.save()

        print("sample data created")

