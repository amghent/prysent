from django.template import defaultfilters
from django.urls import reverse
from django.utils.translation import gettext, ngettext
from jinja2 import Environment
from django.templatetags.static import static


def environment(**options):
    env = Environment(extensions=['jinja2.ext.i18n'], **options)

    env.install_gettext_callables(gettext=gettext, ngettext=ngettext, newstyle=True)

    env.globals.update({
        'static': static,
        'url': reverse,
        'dj': defaultfilters
    })

    return env
