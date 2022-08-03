from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index.html", views.index, name="index"),
    path("layout-static.html", views.layout_static, name="layout_static"),
    path("layout-sidenav-light.html", views.layout_sidenav_light, name="layout_sidenav_light"),
    path("login.html", views.login, name="login"),
    path("password.html", views.password, name="password"),
    path("register.html", views.register, name="register"),
    path("401.html", views.page_401, name="401"),
    path("404.html", views.page_404, name="404"),
    path("500.html", views.page_500, name="500"),
    path("charts.html", views.charts, name="charts"),
    path("tables.html", views.tables, name="tables"),
]
