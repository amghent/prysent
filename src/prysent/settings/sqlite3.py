from prysent.settings.common import *
from prysent.settings.secret import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR.parent.parent, 'database', 'db.sqlite3'),
    },
}

# Get rid of the warning about the un-used import
if DEBUG:
    assert True

if SECRET_KEY == "":
    assert True
