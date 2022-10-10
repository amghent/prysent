import logging

from django.contrib.auth.models import User

from dashboard.models import Dashboard, Link1, Link2, Link3, Block1, Block2
from settings.models import Setting


class Context:
    logger = logging.getLogger(__name__)

    def __init__(self, request) -> None:
        self.logger.debug(f"User: {request.user}")

        # For now, we use user public, until we decide that dashboards can be private again
        self.context = {"user": "Public"}

        # if str(request.user) == "AnonymousUser":
        #    self.context["user"] = "Public"

        #    return

        # self.context = {
        #    "user": self.__user(str(request.user)),
        # }

        # org_units = OrganizationalUnit.filter(members__username=request.user)
        dashboards = Dashboard.objects.all()  # filter(owner__in=org_units).order_by("order")

        self.logger.debug(f"Found {len(dashboards)} dashboards")

        json = []

        for dashboard in dashboards:
            self.logger.debug(f"Generating dashboard: {dashboard.slug}")

            dashboard_json = self.__dashboard(dashboard)

            links = self.__links_1(dashboard)

            if len(links) > 0:
                dashboard_json["links"] = links

            blocks = self.__blocks_1(dashboard)

            if len(blocks) > 0:
                dashboard_json["blocks"] = blocks

            json.append(dashboard_json)

            self.logger.debug(f"JSON for dashboard: {dashboard_json}")

        self.context["dashboards"] = json
        self.context["version"] = Setting.objects.get(key="version").value

    def get(self) -> dict:
        return self.context

    @staticmethod
    def __user(username: str):
        user = User.objects.get(username=username)

        user_json = {
            "username": user.username
        }

        return user_json

    @staticmethod
    def __dashboard(dashboard: Dashboard):
        dashboard_json = {"slug": dashboard.slug, "menu": dashboard.menu, "name": dashboard.name}

        return dashboard_json

    @staticmethod
    def __links_to_menu(links):
        menu = []

        for link in links:
            js = {"slug": link.slug, "menu": link.menu, "data_page": link.data_page.slug}
            menu.append(js)

        return menu

    def __links_1(self, dashboard: Dashboard):
        links = Link1.objects.filter(dashboard=dashboard.id).order_by("slug")
        self.logger.debug(f"Found {len(links)} links on level 1")

        return self.__links_to_menu(links)

    def __links_2(self, block: Block1):
        links = Link2.objects.filter(block1=block.id).order_by("slug")
        self.logger.debug(f"Found {len(links)} links on level 2")

        return self.__links_to_menu(links)

    def __links_3(self, block: Block2):
        links = Link3.objects.filter(block2=block.id).order_by("slug")
        self.logger.debug(f"Found {len(links)} links on level 3")

        return self.__links_to_menu(links)

    def __blocks_1(self, dashboard: Dashboard):
        blocks = Block1.objects.filter(dashboard=dashboard.id).order_by("slug")
        self.logger.debug(f"Found {len(blocks)} blocks on level 1")

        menu = []

        for block in blocks:
            js = {"slug": block.slug, "menu": block.menu, "name": block.name}

            links = self.__links_2(block)

            if len(links) > 0:
                js["links"] = links

            children = self.__blocks_2(block)

            if len(children) > 0:
                js["blocks"] = children

            menu.append(js)

        return menu

    def __blocks_2(self, block: Block1):
        blocks = Block2.objects.filter(block1=block.id).order_by("slug")
        self.logger.debug(f"Found {len(blocks)} blocks on level 2")

        menu = []

        for block in blocks:
            links = self.__links_3(block)

            js = {"slug": block.slug, "menu": block.menu, "name": block.name}

            if len(links) > 0:
                js["links"] = links

            menu.append(js)

        return menu
