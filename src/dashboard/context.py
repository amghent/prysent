from django.contrib.auth.models import User

from dashboard.models import Dashboard, OrganizationalUnit


class Context:
    def __init__(self, request) -> None:
        if str(request.user) == "AnonymousUser":
            self.context = {
                "user": None
            }

            return

        user = User.objects.get(username=str(request.user))

        self.context = {
            "user": user,
        }

        org_units = OrganizationalUnit.objects.filter(members__username=request.user)
        dashboards = Dashboard.objects.filter(owner__in=org_units)

        self.context["dashboards"] = dashboards

    def get(self) -> dict:
        return self.context
