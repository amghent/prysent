from django.contrib.auth.models import User

from dashboard.models import Dashboard, OrganizationalUnit, Level1Link, Level1Menu


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
        dashboard_json = {"id": dashboard.id, "menu": dashboard.menu, "name": dashboard.name, "slug": dashboard.slug}

        return dashboard_json

    @staticmethod
    def __level_1_links_json(dashboard: Dashboard):
        level_1_links = Level1Link.objects.filter(dashboard=dashboard)

        level_1_menu = []

        for link in level_1_links:
            level_1_json = {"id": link.id, "menu": link.menu, "slug": link.slug}
            level_1_menu.append(level_1_json)

        return level_1_menu

    @staticmethod
    def __level_1_menus_json(dashboard: Dashboard):
        level_1_menus = Level1Menu.objects.filter(dashboard=dashboard)

        level_1_menu = []

        for menu in level_1_menus:
            level_1_json = {"id": menu.id, "menu": menu.menu, "slug": menu.slug}
            level_1_menu.append(level_1_json)

        return level_1_menu
