from prysent.settings.common import *
from prysent.settings.secret import *

ALLOWED_HOSTS = []

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

DEBUG = True

if DEBUG:
    INSTALLED_APPS.append('_world_api.apps.WorldApiConfig')

if SECRET_KEY == "":  # Mainly to get rid of the warning about the un-used import
    print("No secret key found")
