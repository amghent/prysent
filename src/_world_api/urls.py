from django.urls import path

from . import views

urlpatterns = [
    path("country/<str:iso>", views.country, name="country"),
    path("country/<str:iso>/population/<int:min_population>", views.large_cities_in_country,
         name="large_cities_in_country"),

    path("city/<str:ascii_name>", views.city_by_name, name="city_by_name"),
]
