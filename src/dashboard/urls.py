from django.urls import path

from . import views

urlpatterns = [
    path("favicon.ico", views.favicon, name="favicon"),

    path("index.html", views.page_index, name="index"),
    path("index.html/<str:status>", views.page_index, name="index"),
    path("", views.page_index, name="index"),

    path("data/<str:slug>", views.page_data, name="data"),

    path("pages/public/<str:slug>", views.public_page, name="public_page"),
    path("pages/auth/<str:slug>", views.authorized_page, name="authorized_page"),

    path("login.html/<str:status>", views.page_login, name="login"),
    path("login.html", views.page_login, name="login"),
    path("login/post", views.action_login_user, name="login_user"),
    path("logout.html", views.action_logout_user, name="logout_user"),

    path("commands/clean_cache", views.clean_cache, name="clean_cache"),
    path("commands/upload_media", views.upload_media, name="upload_media"),
    path("commands/upload_schedule", views.upload_schedule, name="upload_schedule"),
    path("commands/upload_settings", views.upload_settings, name="upload_settings"),
    path("commands/update", views.update, name="update"),

    path("401.html", views.page_401, name="401"),
    path("404.html", views.page_404, name="404"),
    path("500.html", views.page_500, name="500"),

]
