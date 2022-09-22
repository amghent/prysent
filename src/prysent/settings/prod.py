from prysent.settings.common import *
from prysent.settings.secret import *

MEDIA_DIR = os.path.join(Path.home(), 'ArcelorMittal', 'AM Python - Documenten', 'Jobs', 'Automatic_notebooks')
VOILA_URL = "http://notebooks.sidmar.be:8876"

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
