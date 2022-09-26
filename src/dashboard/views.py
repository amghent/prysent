import logging
import os
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate, logout, login
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils.timezone import now

from cacher.models import Cache
from dashboard.context import Context
from dashboard.models import Cardbox, Link3, Link2, Link1, Block1, Block2, DataPage
from dashboard.notebook import Notebook
from scheduler.models import Schedule


logger = logging.getLogger(__name__)


def __render_notebook(path):
    notebook = Notebook(os.path.join(settings.MEDIA_DIR, path))
    html_page = notebook.convert()
    html_page = html_page[len(settings.HTML_DIR)+1:]

    return html_page


def __get_cached(path, cache_minutes=5):
    logger.debug(f"Cached path: {path}")

    try:
        scheduled = Schedule.objects.get(notebook=path)

        if os.path.exists(os.path.join(settings.HTML_DIR, scheduled.html_file)):
            logger.debug(f"returning scheduled file: {scheduled.html_file}")

            return scheduled.html_file

    except Schedule.DoesNotExist:
        pass

    try:
        cached = Cache.objects.get(html_file=path)

        if os.path.exists(os.path.join(settings.HTML_DIR, cached.cached_html)):
            cached.cached_until = now() + timedelta(minutes=cache_minutes)
            cached.save()

            logger.debug(f"returning scheduled file: {cached.cached_html}")

            return cached.cached_html

    except Cache.DoesNotExist:
        pass

    html_page = __render_notebook(path)

    try:
        cache = Cache()
        cache.html_file = path
        cache.cached_until = now() + timedelta(minutes=cache_minutes)
        cache.cached_html = html_page
        cache.save()

    except IntegrityError:
        # In case something goes wrong on writing the cache, we simply ignore
        pass

    return html_page


# @login_required
def page_index(request):
    context = Context(request=request).get()

    html_path = os.path.join("__prysent", "index.ipynb")
    html_page = __get_cached(html_path)

    context["notebook"] = {
        "slug": "index",
        "html": html_page
    }

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

    cardboxes = Cardbox.objects.filter(data_page__slug=slug).order_by("row", "order")
    cardboxes_json = []
    max_row = -1

    for cardbox in cardboxes:
        if cardbox.row > max_row:
            max_row = cardbox.row

        scroll_text = "no"

        if cardbox.scroll:
            scroll_text = "yes"

        cardbox_html = __get_cached(cardbox.notebook)

        cardbox_json = {"id": cardbox.id, "row": cardbox.row, "type": cardbox.type, "title": cardbox.title,
                        "icon": cardbox.icon, "notebook": cardbox_html, "scroll": scroll_text,
                        "height": cardbox.height}

        cardboxes_json.append(cardbox_json)

    context["cardboxes"] = cardboxes_json
    context["cardbox_rows"] = max_row + 1

    try:
        link3 = Link3.objects.get(data_page__slug=slug)
        block2 = Block2.objects.get(id=link3.block2.id)
        block1 = Block1.objects.get(id=block2.block1.id)

        context["breadcrumb"] = {
            "block1": {"slug": block1.slug, "name": block1.name},
            "block2": {"slug": block2.slug, "name": block2.name},
            "link3": {"slug": link3.slug}
        }

    except Link3.DoesNotExist:
        try:
            link2 = Link2.objects.get(data_page__slug=slug)
            block1 = Block1.objects.get(id=link2.block1.id)

            context["breadcrumb"] = {
                "block1": {"slug": block1.slug, "name": block1.name},
                "link2": {"slug": link2.slug}
            }

        except Link2.DoesNotExist:
            link1 = Link1.objects.get(data_page__slug=slug)

            context["breadcrumb"] = {
                "link1": {"slug": link1.slug}
            }

    return render(request=request, template_name="forms/data.jinja2", context=context)


# @login_required
# def page_notebook(request, notebook_path):
#    context = Context(request=request).get()
#
#    html_path = os.path.join(settings.MEDIA_DIR, notebook_path)
#    html_page = __get_cached(html_path)
#
#    context["notebook"] = {
#        "slug": notebook_path,
#        "html": html_page
#    }
#
#    return render(request=request, template_name="forms/notebook.jinja2", context=context)


# def password(request):
#    return render(request=request, template_name="dashboard/password.jinja2", context=None)


# def register(request):
#    return render(request=request, template_name="dashboard/register.jinja2", context=None)


def public_page(request, slug: str):
    context = Context(request=request).get()

    html_path = os.path.join("__prysent", f"{slug}.ipynb")
    html_page = __get_cached(html_path)

    context["notebook"] = {
        "slug": slug,
        "html": html_page
    }

    return render(request=request, template_name="forms/notebook.jinja2", context=context)


# @login_required
def authorized_page(request, slug: str):
    return public_page(request, slug)


def page_401(request):
    context = Context(request=request).get()

    return render(request=request, template_name="forms/401.jinja2", context=context)


def page_404(request):
    context = Context(request=request).get()

    return render(request=request, template_name="forms/404.jinja2", context=context)


def page_500(request):
    context = Context(request=request).get()

    return render(request=request, template_name="forms/500.jinja2", context=context)
