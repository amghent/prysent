from django.http import HttpResponse


def page(request, slug: str):
    html = f"<html><body><p>The page '{slug}' is under construction</p></body></html>"

    return HttpResponse(html)

