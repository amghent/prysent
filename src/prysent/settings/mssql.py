from prysent.settings.common import *
from prysent.settings.secret import *

MEDIA_DIR = os.path.join(BASE_DIR.parent.parent, 'media')
VOILA_URL = "http://localhost:8876"

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

# Get rid of the warning about the un-used import
if DEBUG:
    assert True

if SECRET_KEY == "":
    assert True
