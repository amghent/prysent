from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from dashboard.context import Context


def page_index(request):
    if str(request.user) == "AnonymousUser":
        return redirect(to="login")

    context = Context(request=request).get()

    context["notebook"] = "index"
    context["internal"] = True

    return render(request=request, template_name="dashboard/notebook.jinja2", context=context)


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

    return render(request=request, template_name="dashboard/login.jinja2", context=context)


def action_login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request=request, username=username, password=password)

    print(f"Authenticated user: { user }")

    if user is not None:
        if user.is_active:
            login(request=request, user=user)

            return redirect(to="index")

    return redirect(to="login", status="login=failure")


def action_logout_user(request):
    logout(request=request)

    return redirect(to="login", status="logout=ok")


@login_required
def page_notebook(request, notebook_path):
    context = {
        "notebook": notebook_path,
        "internal": False
    }

    return render(request=request, template_name="dashboard/notebook.jinja2", context=context)


# def password(request):
#    return render(request=request, template_name="dashboard/password.jinja2", context=None)


# def register(request):
#    return render(request=request, template_name="dashboard/register.jinja2", context=None)


def page_401(request):
    return render(request=request, template_name="dashboard/401.jinja2", context=None)


def page_404(request):
    return render(request=request, template_name="dashboard/404.jinja2", context=None)


def page_500(request):
    return render(request=request, template_name="dashboard/500.jinja2", context=None)
