from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def public_page(request, slug: str):
    context = {
        "notebook": slug,
        "internal": True
    }

    return render(request=request, template_name="dashboard/notebook.jinja2", context=context)


@login_required
def authorized_page(request, slug: str):
    context = {
        "notebook": slug,
        "internal": True
    }

    return render(request=request, template_name="dashboard/notebook.jinja2", context=context)

