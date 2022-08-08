from django.urls import path

from . import views

urlpatterns = [
    path("public/<str:slug>", views.public_page, name="public_page"),
    path("auth/<str:slug>", views.authorized_page, name="authorized_page"),
]
