from prysent.settings.common import *
from prysent.settings.secret import *

MEDIA_DIR = os.path.join(BASE_DIR.parent.parent, 'media')
STATICFILES_DIRS.append(os.path.join(MEDIA_DIR, '__prysent'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'prysent-dev',
        'USER': 'prysent',
        'PASSWORD': 'prysent',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# Get rid of the warning about the un-used import
if DEBUG:
    assert True

if SECRET_KEY == "":
    assert True
