from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.context import Context


def public_page(request, slug: str):
    context = Context(request=request).get()

    context["notebook"] = slug,
    context["internal"] = True

    return render(request=request, template_name="dashboard/notebook.jinja2", context=context)


@login_required
def authorized_page(request, slug: str):
    context = Context(request=request).get()

    context["notebook"] = slug,
    context["internal"] = True

    return render(request=request, template_name="dashboard/notebook.jinja2", context=context)
