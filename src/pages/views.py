from django.shortcuts import render


def page(request, slug: str):
    context = {
        "notebook": slug,
        "internal": True
    }

    return render(request=request, template_name="dashboard/notebook.jinja2", context=context)

