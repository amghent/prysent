from prysent.settings.common import *
from prysent.settings.secret import *

MEDIA_DIR = os.path.join(Path.home(), 'ArcelorMittal', 'AM Python - Documenten', 'Jobs',
                         'Belgium', 'Automatic_notebooks')
STATICFILES_DIRS.append(os.path.join(MEDIA_DIR, '__prysent'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR.parent.parent, 'database', 'db.sqlite3'),
    },
}

LOGGING_CONFIG = None

with open(os.path.join(os.path.dirname(__file__), 'logging_prod.yaml'), 'r') as config_file:
    logging_config = yaml.load(config_file, Loader=yaml.FullLoader)

logging.config.dictConfig(logging_config)

# Get rid of the warning about the un-used import
if DEBUG:
    assert True

if SECRET_KEY == "":
    assert True
