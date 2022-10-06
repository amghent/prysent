from prysent.settings.common import *
from prysent.settings.secret import *

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_DIR = os.path.join(BASE_DIR.parent.parent, 'media')
STATICFILES_DIRS.append(os.path.join(MEDIA_DIR, '__prysent'))

DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "prysent",
        "USER": "prysent",
        "PASSWORD": "Prysent_pwd",
        "HOST": "localhost",
        "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server"},
    },
}

LOGGING_CONFIG = None

with open(os.path.join(os.path.dirname(__file__), 'logging.yaml'), 'r') as config_file:
    logging_config = yaml.load(config_file, Loader=yaml.FullLoader)

logging.config.dictConfig(logging_config)

# Get rid of the warning about the un-used import
if DEBUG:
    assert True

if SECRET_KEY == "":
    assert True
