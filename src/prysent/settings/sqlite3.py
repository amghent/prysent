from prysent.settings.common import *
from prysent.settings.secret import *

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR.parent.parent, 'database', 'db.sqlite3'),
    },
}

DEBUG = True

if DEBUG:
    INSTALLED_APPS.append('_world_api.apps.WorldApiConfig')

if SECRET_KEY == "":  # Mainly to get rid of the warning about the un-used import
    print("No secret key found")
