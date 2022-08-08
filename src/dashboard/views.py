from django.shortcuts import render


def index(request):
    context = {
        "notebook": "index",
        "internal": True
    }

    return render(request=request, template_name="dashboard/notebook.jinja2", context=context)


def notebook(request, notebook_path):
    context = {
        "notebook": notebook_path,
        "internal": False
    }

    return render(request=request, template_name="dashboard/notebook.jinja2", context=context)


def login(request):
    return render(request=request, template_name="dashboard/login.jinja2", context=None)


def password(request):
    return render(request=request, template_name="dashboard/password.jinja2", context=None)


def register(request):
    return render(request=request, template_name="dashboard/register.jinja2", context=None)


def page_401(request):
    return render(request=request, template_name="dashboard/401.jinja2", context=None)


def page_404(request):
    return render(request=request, template_name="dashboard/404.jinja2", context=None)


def page_500(request):
    return render(request=request, template_name="dashboard/500.jinja2", context=None)


def charts(request):
    return render(request=request, template_name="dashboard/demo/charts.jinja2", context=None)


def tables(request):
    return render(request=request, template_name="dashboard/demo/tables.jinja2", context=None)
