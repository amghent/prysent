import logging

from django.contrib.auth.models import User

from _world_api.models import City
from dashboard.models import CardboxType, OrganizationalUnit, Dashboard, DataPage, Link1, Block1, Link2, Block2, \
    Link3, Cardbox

from configurator.utils import Utils as ConfiguratorUtils


class Utils:
    logger = logging.getLogger(__name__)

    @classmethod
    def upload(cls):
        cls.__upload_users()
        cls.__upload_ou()
        cls.__upload_dashboards()  # depends on ou
        cls.__upload_data_pages()
        cls.__upload_links_1()  # depends on dashboards and data_pages
        cls.__upload_blocks_1()  # depends on dashboards
        cls.__upload_links_2()  # depends on blocks_1 and data_pages
        cls.__upload_blocks_2()  # depends on blocks1_1
        cls.__upload_links_3()  # depends on blocks_2 and data_pages
        cls.__upload_cardbox_types()
        cls.__upload_cardboxes()  # depends on cardbox_types and data_pages

    @classmethod
    def __upload_users(cls):
        rows = ConfiguratorUtils.read_csv("users.csv", "")

        for row in rows:
            u = User()

            u.username, u.first_name, u.last_name, u.email = tuple(row)
            u.set_password("password")
            # Must use set_password to pass unencrypted pwd, not user.password=xyz

            u.save()

    @classmethod
    def __upload_ou(cls):
        rows = ConfiguratorUtils.read_csv("ou.csv", "")

        for row in rows:
            u = OrganizationalUnit()

            u.name, u.slug, members = tuple(row)

            u.save()

            for member in members.split(";"):
                m = User.objects.get(username=member)
                u.members.add(m)

    @classmethod
    def __upload_dashboards(cls):
        rows = ConfiguratorUtils.read_csv("dashboards.csv", "")

        for row in rows:
            d = Dashboard()

            d.name, d.slug, d.menu, ou, d.order = tuple(row)
            d.owner = OrganizationalUnit.objects.get(slug=ou)

            d.save()

    @classmethod
    def __upload_data_pages(cls):
        rows = ConfiguratorUtils.read_csv("data_pages.csv", "")

        for row in rows:
            p = DataPage()

            p.slug, p.title = tuple(row)

            p.save()

    @classmethod
    def __upload_links_1(cls):
        rows = ConfiguratorUtils.read_csv("links_1.csv", "")

        for row in rows:
            i = Link1()

            i.slug, i.menu, dashboard, data, i.order = tuple(row)
            i.dashboard = Dashboard.objects.get(slug=dashboard)
            i.data_page = DataPage.objects.get(slug=data)

            i.save()

    @classmethod
    def __upload_blocks_1(cls):
        rows = ConfiguratorUtils.read_csv("blocks_1.csv", "")

        for row in rows:
            b = Block1()

            b.slug, b.menu, db, b.order = tuple(row)
            b.dashboard = Dashboard.objects.get(slug=db)

            b.save()

    @classmethod
    def __upload_links_2(cls):
        rows = ConfiguratorUtils.read_csv("links_2.csv", "")

        for row in rows:
            i = Link2()

            i.slug, i.menu, block, data, i.order = tuple(row)
            i.block1 = Block1.objects.get(slug=block)
            i.data_page = DataPage.objects.get(slug=data)

            i.save()

    @classmethod
    def __upload_blocks_2(cls):
        rows = ConfiguratorUtils.read_csv("blocks_2.csv", "")

        for row in rows:
            b = Block2()

            b.slug, b.menu, block, b.order = tuple(row)
            b.block1 = Block1.objects.get(slug=block)

            b.save()

    @classmethod
    def __upload_links_3(cls):
        rows = ConfiguratorUtils.read_csv("links_3.csv", "")

        for row in rows:
            i = Link3()

            i.slug, i.menu, block, data, i.order = tuple(row)
            i.block2 = Block2.objects.get(slug=block)
            i.data_page = DataPage.objects.get(slug=data)

            i.save()

    @classmethod
    def __upload_cardbox_types(cls):
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

    @classmethod
    def __upload_cardboxes(cls):
        rows = ConfiguratorUtils.read_csv("cardboxes.csv", "")

        for row in rows:
            c = Cardbox()

            c.row, c.order, cb_type, c.height, c.title, c.icon, c.notebook, data = tuple(row)
            c.type = CardboxType.objects.get(slug=cb_type)
            c.data_page = DataPage.objects.get(slug=data)

            c.save()

    @classmethod
    def upload_world_cities(cls):
        rows = ConfiguratorUtils.read_csv("world_cities.csv", 0)

        for row in rows:
            c = City()

            c.name, c.name_ascii, c.lat, c.lng, c.country, c.iso2, c.iso3, c.admin_name, \
                c.capital, c.population, c.id = tuple(row)

            if c.iso2 == "BE":
                c.save()
