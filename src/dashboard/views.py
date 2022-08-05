from django.shortcuts import render


def index(request):
    return render(request=request, template_name="dashboard/index.jinja2", context=None)


def layout_static(request):
    return render(request=request, template_name="forms/layout-static.jinja2", context=None)


def login(request):
    return render(request=request, template_name="forms/login.html", context=None)


def password(request):
    return render(request=request, template_name="forms/password.html", context=None)


def register(request):
    return render(request=request, template_name="forms/register.html", context=None)


def page_401(request):
    return render(request=request, template_name="dashboard/401.jinja2", context=None)


def page_404(request):
    return render(request=request, template_name="dashboard/404.jinja2", context=None)


def page_500(request):
    return render(request=request, template_name="dashboard/500.jinja2", context=None)


def charts(request):
    return render(request=request, template_name="dashboard/demo/charts.jinja2", context=None)


def tables(request):
    return render(request=request, template_name="forms/tables.html", context=None)
