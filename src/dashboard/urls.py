from django.urls import path

from . import views

urlpatterns = [
    path("index.html", views.page_index, name="index"),
    path("", views.page_index, name="index"),

    path("login.html/<str:status>", views.page_login, name="login"),
    path("login.html", views.page_login, name="login"),
    path("login/post", views.action_login_user, name="login_user"),
    path("logout.html", views.action_logout_user, name="logout_user"),

    # path("password.html", views.password, name="password"),
    # path("register.html", views.register, name="register"),

    path("401.html", views.page_401, name="401"),
    path("404.html", views.page_404, name="404"),
    path("500.html", views.page_500, name="500"),

    path("notebook/<str:notebook_path>", views.page_notebook, name="notebook"),
    path("data/<str:dashboard>/<str:slug>", views.page_data, name="data"),

    path("pages/public/<str:slug>", views.public_page, name="public_page"),
    path("pages/auth/<str:slug>", views.authorized_page, name="authorized_page"),
]
