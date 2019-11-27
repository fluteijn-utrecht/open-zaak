import datetime
import os

from django.urls import reverse_lazy

import raven

from .api import *  # noqa
from .environ import config
from .plugins import PLUGIN_INSTALLED_APPS

# Build paths inside the project, so further paths can be defined relative to
# the code root.
DJANGO_PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
)
BASE_DIR = os.path.abspath(
    os.path.join(DJANGO_PROJECT_DIR, os.path.pardir, os.path.pardir)
)

#
# Core Django settings
#
SITE_ID = config("SITE_ID", default=1)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# NEVER run with DEBUG=True in production-like environments
DEBUG = config("DEBUG", default=False)

# = domains we're running on
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", split=True)

IS_HTTPS = config("IS_HTTPS", default=not DEBUG)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "nl-nl"

TIME_ZONE = "UTC"  # note: this *may* affect the output of DRF datetimes

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

#
# DATABASE and CACHING setup
#
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config("DB_NAME", "openzaak"),
        "USER": config("DB_USER", "openzaak"),
        "PASSWORD": config("DB_PASSWORD", "openzaak"),
        "HOST": config("DB_HOST", "localhost"),
        "PORT": config("DB_PORT", 5432),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('CACHE_DEFAULT', 'localhost:6379/0')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
    "axes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('CACHE_AXES', 'localhost:6379/0')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
}

#
# APPLICATIONS enabled for this project
#
INSTALLED_APPS = [
    # Note: contenttypes should be first, see Django ticket #10827
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    # Note: If enabled, at least one Site object is required
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Optional applications.
    "ordered_model",
    "django_admin_index",
    "django.contrib.admin",
    "django.contrib.gis",
    # 'django.contrib.admindocs',
    # 'django.contrib.humanize',
    # External applications.
    "axes",
    "django_filters",
    "corsheaders",
    "vng_api_common",  # before drf_yasg to override the management command
    "vng_api_common.authorizations",
    "vng_api_common.audittrails",
    "vng_api_common.notifications",
    "drf_yasg",
    "rest_framework",
    "rest_framework_gis",
    "django_markup",
    "solo",
    "privates",
    "django_better_admin_arrayfield.apps.DjangoBetterAdminArrayfieldConfig",
    "django_loose_fk",
    # Project applications.
    "openzaak",
    "openzaak.accounts",
    "openzaak.utils",
    "openzaak.components.authorizations",
    "openzaak.components.zaken",
    "openzaak.components.besluiten",
    "openzaak.components.documenten",
    "openzaak.components.catalogi",
    "openzaak.selectielijst.apps.SelectielijstConfig",
] + PLUGIN_INSTALLED_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "openzaak.utils.middleware.LogHeadersMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # 'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "openzaak.components.authorizations.middleware.AuthMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "vng_api_common.middleware.APIVersionHeaderMiddleware",
]

ROOT_URLCONF = "openzaak.urls"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(DJANGO_PROJECT_DIR, "templates")],
        "APP_DIRS": False,  # conflicts with explicity specifying the loaders
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "openzaak.utils.context_processors.settings",
                "django_admin_index.context_processors.dashboard",
            ],
            "loaders": TEMPLATE_LOADERS,
        },
    }
]

WSGI_APPLICATION = "openzaak.wsgi.application"

# Translations
LOCALE_PATHS = (os.path.join(DJANGO_PROJECT_DIR, "conf", "locale"),)

#
# SERVING of static and media files
#

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Additional locations of static files
STATICFILES_DIRS = [os.path.join(DJANGO_PROJECT_DIR, "static")]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"

#
# Sending EMAIL
#
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config(
    "EMAIL_PORT", default=25
)  # disabled on Google Cloud, use 487 instead
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False)
EMAIL_TIMEOUT = 10

DEFAULT_FROM_EMAIL = "openzaak@example.com"

#
# LOGGING
#
LOGGING_DIR = os.path.join(BASE_DIR, "log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(process)d %(thread)d  %(message)s"
        },
        "timestamped": {"format": "%(asctime)s %(levelname)s %(name)s  %(message)s"},
        "simple": {"format": "%(levelname)s  %(message)s"},
        "performance": {"format": "%(asctime)s %(process)d | %(thread)d | %(message)s"},
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "timestamped",
        },
        "django": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "django.log"),
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "project": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "openzaak.log"),
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "performance": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "performance.log"),
            "formatter": "performance",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "requests": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "requests.log"),
            "formatter": "timestamped",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
    },
    "loggers": {
        "openzaak": {"handlers": ["project"], "level": "INFO", "propagate": True},
        "openzaak.utils.middleware": {
            "handlers": ["requests"],
            "level": "DEBUG",
            "propagate": False,
        },
        "vng_api_common": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django.request": {"handlers": ["django"], "level": "ERROR", "propagate": True},
        "django.template": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}


#
# AUTH settings - user accounts, passwords, backends...
#
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Allow logging in with both username+password and email+password
AUTHENTICATION_BACKENDS = [
    "openzaak.accounts.backends.UserModelEmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

SESSION_COOKIE_NAME = "openzaak_sessionid"

#
# SECURITY settings
#
SESSION_COOKIE_SECURE = IS_HTTPS
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = IS_HTTPS

X_FRAME_OPTIONS = "DENY"

#
# Silenced checks
#
SILENCED_SYSTEM_CHECKS = ["rest_framework.W001"]

#
# Custom settings
#
PROJECT_NAME = "Open Zaak"
SITE_TITLE = "API dashboard"

ENVIRONMENT = None
ENVIRONMENT_SHOWN_IN_ADMIN = True

# settings for uploading large files
MIN_UPLOAD_SIZE = config("MIN_UPLOAD_SIZE", 4 * 2 ** 30)

# urls for OAS3 specifications
SPEC_URL = {
    "zaken": os.path.join(
        BASE_DIR, "src", "openzaak", "components", "zaken", "openapi.yaml"
    ),
    "besluiten": os.path.join(
        BASE_DIR, "src", "openzaak", "components", "besluiten", "openapi.yaml"
    ),
    "documenten": os.path.join(
        BASE_DIR, "src", "openzaak", "components", "documenten", "openapi.yaml"
    ),
    "catalogi": os.path.join(
        BASE_DIR, "src", "openzaak", "components", "catalogi", "openapi.yaml"
    ),
    "authorizations": os.path.join(
        BASE_DIR, "src", "openzaak", "components", "authorizations", "openapi.yaml"
    ),
}

# Generating the schema, depending on the component
subpath = config("SUBPATH", None)
if subpath:
    if not subpath.startswith("/"):
        subpath = f"/{subpath}"
    FORCE_SCRIPT_NAME = subpath

if "GIT_SHA" in os.environ:
    GIT_SHA = config("GIT_SHA", "")
# in docker (build) context, there is no .git directory
elif os.path.exists(os.path.join(BASE_DIR, ".git")):
    GIT_SHA = raven.fetch_git_sha(BASE_DIR)
else:
    GIT_SHA = None

##############################
#                            #
# 3RD PARTY LIBRARY SETTINGS #
#                            #
##############################

#
# DJANGO-AXES
#
AXES_CACHE = "axes"  # refers to CACHES setting
AXES_LOGIN_FAILURE_LIMIT = 5  # Default: 3
AXES_LOCK_OUT_AT_FAILURE = True  # Default: True
AXES_USE_USER_AGENT = False  # Default: False
AXES_COOLOFF_TIME = datetime.timedelta(minutes=5)  # One hour
AXES_BEHIND_REVERSE_PROXY = IS_HTTPS  # We have either Ingress or Nginx
AXES_ONLY_USER_FAILURES = (
    False  # Default: False (you might want to block on username rather than IP)
)
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = (
    False  # Default: False (you might want to block on username and IP)
)

#
# DJANGO-HIJACK
#
HIJACK_LOGIN_REDIRECT_URL = reverse_lazy("home")
HIJACK_LOGOUT_REDIRECT_URL = reverse_lazy("admin:accounts_user_changelist")
HIJACK_REGISTER_ADMIN = False
# This is a CSRF-security risk.
# See: http://django-hijack.readthedocs.io/en/latest/configuration/#allowing-get-method-for-hijack-views
HIJACK_ALLOW_GET_REQUESTS = True

#
# DJANGO-CORS-MIDDLEWARE
#
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    "x-requested-with",
    "content-type",
    "accept",
    "origin",
    "authorization",
    "x-csrftoken",
    "user-agent",
    "accept-encoding",
    "accept-crs",
    "content-crs",
)

#
# DJANGO-PRIVATES -- safely serve files after authorization
#
PRIVATE_MEDIA_ROOT = os.path.join(BASE_DIR, "private-media")
PRIVATE_MEDIA_URL = "/private-media/"

# requires an nginx container running in front
SENDFILE_BACKEND = config("SENDFILE_BACKEND", "sendfile.backends.nginx")
SENDFILE_ROOT = PRIVATE_MEDIA_ROOT
SENDFILE_URL = PRIVATE_MEDIA_URL

#
# DJANGO-LOOSE-FK -- handle internal and external API resources
#
DEFAULT_LOOSE_FK_LOADER = "openzaak.loaders.AuthorizedRequestsLoader"

#
# RAVEN/SENTRY - error monitoring
#
SENTRY_DSN = config("SENTRY_DSN", None)

if SENTRY_DSN:
    INSTALLED_APPS = INSTALLED_APPS + ["raven.contrib.django.raven_compat"]

    RAVEN_CONFIG = {"dsn": SENTRY_DSN, "release": GIT_SHA}
    LOGGING["handlers"].update(
        {
            "sentry": {
                "level": "WARNING",
                "class": "raven.handlers.logging.SentryHandler",
                "dsn": RAVEN_CONFIG["dsn"],
            }
        }
    )

#
# DJANGO-ADMIN-INDEX
#
ADMIN_INDEX_SHOW_REMAINING_APPS_TO_SUPERUSERS = False
ADMIN_INDEX_AUTO_CREATE_APP_GROUP = False