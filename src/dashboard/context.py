from pprint import pprint

from django.contrib.auth.models import User

from dashboard.models import Dashboard, OrganizationalUnit, Link1, Link2, Link3, Block1, Block2


class Context:
    def __init__(self, request) -> None:
        if str(request.user) == "AnonymousUser":
            self.context = {
                "user": None
            }

            return

        self.context = {
            "user": self.__user_json(str(request.user)),
        }

        org_units = OrganizationalUnit.objects.filter(members__username=request.user)
        dashboards = Dashboard.objects.filter(owner__in=org_units)

        json = []

        for dashboard in dashboards:
            dashboard_json = self.__dashboard_json(dashboard)

            dashboard_json["links"] = self.__level_1_links_json(dashboard)
            dashboard_json["blocks"] = self.__level_1_blocks_json(dashboard)

            json.append(dashboard_json)

        pprint(json)
        self.context["dashboards"] = json

    def get(self) -> dict:
        return self.context

    @staticmethod
    def __user_json(username: str):
        user = User.objects.get(username=username)

        user_json = {
            "username": user.username
        }

        return user_json

    @staticmethod
    def __dashboard_json(dashboard: Dashboard):
        dashboard_json = {"slug": dashboard.slug, "menu": dashboard.menu, "name": dashboard.name}

        return dashboard_json

    @staticmethod
    def __level_1_links_json(dashboard: Dashboard):
        links = Link1.objects.filter(dashboard=dashboard)
        menu = []

        for link in links:
            js = {"slug": link.slug, "menu": link.menu, "data_page": link.data_page}
            menu.append(js)

        return menu

    def __level_1_blocks_json(self, dashboard: Dashboard):
        blocks = Block1.objects.filter(dashboard=dashboard)
        menu = []

        for block in blocks:
            js = {"slug": block.slug, "menu": block.menu}

            links = self.__level_2_links_json(block)

            if len(links) > 0:
                js["links"] = links

            children = self.__level_2_blocks_json(block)

            if len(children) > 0:
                js["blocks"] = children

            menu.append(js)

        return menu

    @staticmethod
    def __level_2_links_json(link_1: Link1):
        links = Link2.objects.filter(link1=link_1)
        menu = []

        for link in links:
            js = {"slug": link.slug, "menu": link.menu, "data_page": link.data_page}
            menu.append(js)

        return menu

    def __level_2_blocks_json(self, block_1: Block1):
        blocks = Block2.objects.filter(block1=block_1)
        menu = []

        for block in blocks:
            links = self.__level_3_links_json(block)

            js = {"slug": block.slug, "menu": block.menu}

            if len(links) > 0:
                js["links"] = links

            menu.append(js)

        return menu

    @staticmethod
    def __level_3_links_json(link_2: Link2):
        links = Link3.objects.filter(link2=link_2)
        menu = []

        for link in links:
            js = {"slug": link.slug, "menu": link.menu, "data_page": link.data_page}
            menu.append(js)

        return menu
