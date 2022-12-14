import os

from pathlib import Path

DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    '_commands.apps.CommandsConfig',
    '_samples.apps.SamplesConfig',

    'cacher.apps.CacherConfig',
    'configurator.apps.ConfiguratorConfig',
    'dashboard.apps.DashboardConfig',
    'media.apps.MediaConfig',
    'settings.apps.SettingsConfig',
    'scheduler.apps.SchedulerConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR.parent, '_templates', 'arcelor_mittal'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'prysent.jinja2.environment'
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'prysent.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ALLOWED_HOSTS = ["*"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'prysent.urls'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR.parent, '_templates', 'arcelor_mittal', 'static'),
]

HTML_DIR = os.path.join(BASE_DIR.parent, '_html_cache')
COMMANDS_DIR = os.path.join(BASE_DIR.parent, "_commands")

STATIC_ROOT = HTML_DIR

if DEBUG:
    INSTALLED_APPS.append('_world_api.apps.WorldApiConfig')
