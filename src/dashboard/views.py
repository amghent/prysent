from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from dashboard.context import Context
from dashboard.models import Cardbox


@login_required
def page_index(request):
    context = Context(request=request).get()

    context["notebook"] = {
        "slug": "index",
        "internal": True
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


@login_required
def page_data(request, slug):
    # slug is the data_page slug
    context = Context(request=request).get()

    cardboxes = Cardbox.objects.filter(notebook_page__slug=slug)
    cardboxes_json = []
    max_row = -1
    heights = []

    for cardbox in cardboxes:
        if cardbox.row > max_row:
            max_row = cardbox.row

        while len(heights) <= cardbox.row:
            heights.append(0)

        heights[cardbox.row] = cardbox.height

        cardbox_json = {"id": cardbox.id, "row": cardbox.row, "type": cardbox.type, "title": cardbox.title,
                        "icon": cardbox.icon, "notebook": cardbox.notebook}

        cardboxes_json.append(cardbox_json)

    context["cardboxes"] = cardboxes_json
    context["cardbox_rows"] = max_row + 1
    context["cardbox_heights"] = heights

    return render(request=request, template_name="forms/data.jinja2", context=context)


@login_required
def page_notebook(request, notebook_path):
    context = Context(request=request).get()

    context["notebook"] = {
        "slug": notebook_path,
        "internal": False
    }

    return render(request=request, template_name="forms/notebook.jinja2", context=context)


# def password(request):
#    return render(request=request, template_name="dashboard/password.jinja2", context=None)


# def register(request):
#    return render(request=request, template_name="dashboard/register.jinja2", context=None)


def public_page(request, slug: str):
    context = Context(request=request).get()

    context["notebook"] = {
        "slug": slug,
        "internal": True
    }

    return render(request=request, template_name="forms/notebook.jinja2", context=context)


@login_required
def authorized_page(request, slug: str):
    context = Context(request=request).get()

    context["notebook"] = {
        "slug": slug,
        "internal": True
    }

    return render(request=request, template_name="forms/notebook.jinja2", context=context)


def page_401(request):
    context = Context(request=request).get()

    return render(request=request, template_name="forms/401.jinja2", context=context)


def page_404(request):
    context = Context(request=request).get()

    return render(request=request, template_name="forms/404.jinja2", context=context)


def page_500(request):
    context = Context(request=request).get()

    return render(request=request, template_name="forms/500.jinja2", context=context)
