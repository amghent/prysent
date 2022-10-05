import logging
import os

from django.conf import settings
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect

import cacher.utils
import configurator.utils
import media.utils
import scheduler.utils
from dashboard.context import Context
from dashboard.models import Cardbox, Link3, Link2, Link1, Block1, Block2, DataPage, Dashboard

from cacher.utils import CACHER_GENERATION_TIMEOUT, CACHER_GENERATION_ERROR

logger = logging.getLogger(__name__)


# @login_required
def page_index(request):
    html_path = os.path.join("__prysent", "index.ipynb")
    html_page, cached, message = cacher.utils.Utils.get_cached_html(html_path)

    context = Context(request=request).get()

    context["notebook"] = {
        "slug": "index",
        "html": html_page
    }
    context["message"] = message

    if html_page == CACHER_GENERATION_ERROR:
        return render(request=request, template_name="forms/error.jinja2", context=context)

    if html_page == CACHER_GENERATION_TIMEOUT:
        return render(request=request, template_name="forms/timeout.jinja2", context=context)

    if cached is False:
        return render(request=request, template_name="forms/wait.jinja2", context=context)

    return render(request=request, template_name="forms/notebook.jinja2", context=context)


def page_login(request, status: str = None):
    context = Context(request=request).get()

    if status == "login=failure":
        context["message"] = {
            "color": "text-danger",
            "text": "User name or password are incorrect. Try again."
        }

    if status == "logout=ok":
        context["message"] = {
            "color": "text-success",
            "text": "You are now logged out."
        }

    return render(request=request, template_name="forms/login.jinja2", context=context)


def action_login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request=request, username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request=request, user=user)

            return redirect(to="index")

    return redirect(to="login", status="login=failure")


def action_logout_user(request):
    logout(request=request)

    return redirect(to="login", status="logout=ok")


#  @login_required
def page_data(request, slug):
    # slug is the data_page slug
    context = Context(request=request).get()

    data_page = DataPage.objects.get(slug=slug)

    context["title"] = data_page.title
    context["slug"] = data_page.slug
    context["message"] = ""

    cardboxes = Cardbox.objects.filter(data_page__slug=slug).order_by("row", "order")
    cardboxes_json = []
    max_row = -1

    cardbox_html = ""
    cached = True
    message = ""

    for cardbox in cardboxes:
        if cardbox.row > max_row:
            max_row = cardbox.row

        scroll_text = "no"

        if cardbox.scroll:
            scroll_text = "yes"

        cardbox_html, cached, message = cacher.utils.Utils.get_cached_html(cardbox.notebook)

        cardbox_json = {"id": cardbox.id, "row": cardbox.row, "type": cardbox.type, "title": cardbox.title,
                        "icon": cardbox.icon, "notebook": cardbox_html, "scroll": scroll_text,
                        "height": cardbox.height}

        cardboxes_json.append(cardbox_json)

        if cardbox_html == CACHER_GENERATION_ERROR:
            context["message"] = message

            break

    context["cardboxes"] = cardboxes_json
    context["cardbox_rows"] = max_row + 1

    try:
        link3 = Link3.objects.get(data_page__slug=slug)
        block2 = Block2.objects.get(id=link3.block2.id)
        block1 = Block1.objects.get(id=block2.block1.id)
        dashboard = Dashboard.objects.get(id=block1.dashboard.id)

        context["breadcrumb"] = {
            "dashboard": {"slug": dashboard.slug, "name": dashboard.name},
            "block1": {"slug": block1.slug, "name": block1.name},
            "block2": {"slug": block2.slug, "name": block2.name},
            "link3": {"slug": link3.slug}
        }

    except Link3.DoesNotExist:
        try:
            link2 = Link2.objects.get(data_page__slug=slug)
            block1 = Block1.objects.get(id=link2.block1.id)
            dashboard = Dashboard.objects.get(id=block1.dashboard.id)

            context["breadcrumb"] = {
                "dashboard": {"slug": dashboard.slug, "name": dashboard.name},
                "block1": {"slug": block1.slug, "name": block1.name},
                "link2": {"slug": link2.slug}
            }

        except Link2.DoesNotExist:
            link1 = Link1.objects.get(data_page__slug=slug)
            dashboard = Dashboard.objects.get(id=link1.dashboard.id)

            context["breadcrumb"] = {
                "dashboard": {"slug": dashboard.slug, "name": dashboard.name},
                "link1": {"slug": link1.slug}
            }

    if message != "":
        return render(request=request, template_name="forms/error.jinja2", context=context)

    if cardbox_html == CACHER_GENERATION_TIMEOUT:
        return render(request=request, template_name="forms/timeout.jinja2", context=context)

    if cached is False:
        return render(request=request, template_name="forms/wait.jinja2", context=context)

    return render(request=request, template_name="forms/data.jinja2", context=context)


def public_page(request, slug: str):
    html_path = os.path.join("__prysent", f"{slug}.ipynb")
    html_page, cached, message = cacher.utils.Utils.get_cached_html(html_path)

    context = Context(request=request).get()

    context["notebook"] = {
        "slug": slug,
        "html": html_page
    }
    context["message"] = message

    if html_page == CACHER_GENERATION_ERROR:
        return render(request=request, template_name="forms/error.jinja2", context=context)

    if html_page == CACHER_GENERATION_TIMEOUT:
        return render(request=request, template_name="forms/timeout.jinja2", context=context)

    if cached is False:
        return render(request=request, template_name="forms/wait.jinja2", context=context)

    return render(request=request, template_name="forms/notebook.jinja2", context=context)


# @login_required
def authorized_page(request, slug: str):
    return public_page(request, slug)


def clean_cache(request):
    cacher.utils.Utils.clean_cache()

    return redirect("index")


def upload_media(request):
    media.utils.Utils.upload()

    return redirect("index")


def upload_schedule(request):
    configurator.utils.Utils.check_directory(settings.MEDIA_DIR)

    return redirect("index")


def update(request):
    scheduler.utils.Utils.update_scheduled_notebooks()
    scheduler.utils.Utils.remove_cached_notebooks()

    return redirect("index")


def page_401(request):
    context = Context(request=request).get()

    return render(request=request, template_name="forms/401.jinja2", context=context)


def page_404(request):
    context = Context(request=request).get()

    return render(request=request, template_name="forms/404.jinja2", context=context)


def page_500(request):
    context = Context(request=request).get()

    return render(request=request, template_name="forms/500.jinja2", context=context)
