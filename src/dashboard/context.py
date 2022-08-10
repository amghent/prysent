from pprint import pprint

from django.contrib.auth.models import User

from dashboard.models import Dashboard, OrganizationalUnit, Level1Link, Level1Menu, Level2Link, Level2Menu, Level3Link


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

            dashboard_json["menu_items"] = self.__level_1_links_json(dashboard)
            dashboard_json["menu_blocks"] = self.__level_1_menus_json(dashboard)

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
        dashboard_json = {"level": 0, "type": "dashboard", "id": dashboard.id, "menu": dashboard.menu,
                          "name": dashboard.name, "slug": dashboard.slug}

        return dashboard_json

    @staticmethod
    def __level_1_links_json(dashboard: Dashboard):
        level_1_links = Level1Link.objects.filter(dashboard=dashboard)
        level_1_menu = []

        for link in level_1_links:
            level_1_json = {"level": 1, "type": "link", "id": link.id, "menu": link.menu, "slug": link.slug}
            level_1_menu.append(level_1_json)

        return level_1_menu

    def __level_1_menus_json(self, dashboard: Dashboard):
        level_1_menus = Level1Menu.objects.filter(dashboard=dashboard)
        level_1_menu = []

        for menu in level_1_menus:
            level_1_json = {"level": 1, "type": "menu", "id": menu.id, "menu": menu.menu, "slug": menu.slug}

            menu_items = self.__level_2_links_json(menu)

            if len(menu_items) > 0:
                level_1_json["menu_items"] = menu_items

            menu_blocks = self.__level_2_menus_json(menu)

            if len(menu_blocks) > 0:
                level_1_json["menu_blocks"] = menu_blocks

            level_1_menu.append(level_1_json)

        return level_1_menu

    @staticmethod
    def __level_2_links_json(menu_1: Level1Menu):
        level_2_links = Level2Link.objects.filter(level1menu=menu_1)
        level_2_menu = []

        for link in level_2_links:
            level_2_json = {"level": 2, "type": "link", "id": link.id, "menu": link.menu, "slug": link.slug}
            level_2_menu.append(level_2_json)

        return level_2_menu

    def __level_2_menus_json(self, menu_1: Level1Menu):
        level_2_menus = Level2Menu.objects.filter(level1menu=menu_1)
        level_2_menu = []

        for menu in level_2_menus:
            menu_items = self.__level_3_links_json(menu)

            level_2_json = {"level": 2, "type": "menu", "id": menu.id, "menu": menu.menu, "slug": menu.slug}

            if len(menu_items) > 0:
                level_2_json["menu_items"] = menu_items

            level_2_menu.append(level_2_json)

        return level_2_menu

    @staticmethod
    def __level_3_links_json(menu_2: Level2Menu):
        level_3_links = Level3Link.objects.filter(level2menu=menu_2)
        level_3_menu = []

        for link in level_3_links:
            level_3_json = {"level": 3, "type": "link", "id": link.id, "menu": link.menu, "slug": link.slug}
            level_3_menu.append(level_3_json)

        return level_3_menu
