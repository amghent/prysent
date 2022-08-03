from django.http import JsonResponse

from _world_api.models import City


def country(request, iso: str):
    records = list(City.objects.filter(iso2__iexact=iso).values() | City.objects.filter(iso3=iso).values())

    return JsonResponse(records, safe=False)


def city_by_name(request, ascii_name: str):
    records = list(City.objects.filter(name_ascii__iexact=ascii_name).values())

    return JsonResponse(records, safe=False)


def large_cities_in_country(request, iso: str, min_population: int):
    records = list(City.objects.filter(population__gte=min_population, iso2__iexact=iso).values() |
                   City.objects.filter(population__gte=min_population, iso3__iexact=iso).values())

    return JsonResponse(records, safe=False)
