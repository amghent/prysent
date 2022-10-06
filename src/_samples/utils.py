import logging

from _world_api.models import City

from configurator.utils import Utils as ConfiguratorUtils


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def upload_world_cities(cls):
        rows = ConfiguratorUtils.read_csv("world_cities.csv", 0)

        cls.logger.debug(f"Found total rows: {len(rows)}")

        for row in rows:
            c = City()

            c.name, c.name_ascii, c.lat, c.lng, c.country, c.iso2, c.iso3, c.admin_name, \
                c.capital, c.population, c.id = tuple(row)

            if c.iso2 == "BE":
                c.save()
