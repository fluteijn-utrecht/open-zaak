# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2019 - 2022 Dimpact
import datetime
import os
import warnings

from django.urls import reverse_lazy

import sentry_sdk
from corsheaders.defaults import default_headers as default_cors_headers
from log_outgoing_requests.formatters import HttpFormatter
from notifications_api_common.settings import *  # noqa

from ...utils.monitoring import filter_sensitive_data
from .api import *  # noqa
from .environ import config, get_sentry_integrations, strip_protocol_from_origin
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
USE_X_FORWARDED_HOST = config("USE_X_FORWARDED_HOST", default=False)

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

# Geospatial libraries
GEOS_LIBRARY_PATH = config("GEOS_LIBRARY_PATH", None)
GDAL_LIBRARY_PATH = config("GDAL_LIBRARY_PATH", None)

# TODO: after the 3.2 upgrade at some point we'll switch this to BigAutoField which will
# become the default in Django
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

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
    "oidc": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('CACHE_DEFAULT', 'localhost:6379/0')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
    "import_requests": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "import_requests",
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
    "django_db_logger",
    "corsheaders",
    "extra_views",
    "vng_api_common",
    "vng_api_common.authorizations",
    "vng_api_common.audittrails",
    "vng_api_common.notifications",
    "notifications_api_common",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_gis",
    "django_markup",
    "solo",
    "sniplates",
    "privates",
    "django_better_admin_arrayfield",
    "django_jsonform",
    "django_loose_fk",
    "simple_certmanager",
    "zgw_consumers",
    "drc_cmis",
    "mozilla_django_oidc",
    "mozilla_django_oidc_db",
    "log_outgoing_requests",
    "django_setup_configuration",
    # Project applications.
    "openzaak",
    "openzaak.accounts",
    "openzaak.utils",
    "openzaak.components.autorisaties",
    "openzaak.components.zaken",
    "openzaak.components.besluiten",
    "openzaak.components.documenten",
    "openzaak.components.catalogi",
    "openzaak.config",
    "openzaak.selectielijst",
    "openzaak.notifications",
] + PLUGIN_INSTALLED_APPS

MIDDLEWARE = [
    "openzaak.utils.middleware.OverrideHostMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "openzaak.utils.middleware.LogHeadersMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # 'django.middleware.locale.LocaleMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "openzaak.components.autorisaties.middleware.AuthMiddleware",
    "mozilla_django_oidc_db.middleware.SessionRefresh",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "openzaak.utils.middleware.APIVersionHeaderMiddleware",
    "openzaak.utils.middleware.DeprecationMiddleware",
    "openzaak.utils.middleware.EnabledMiddleware",
    "axes.middleware.AxesMiddleware",
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
LOG_STDOUT = config("LOG_STDOUT", default=False)
LOG_LEVEL = config("LOG_LEVEL", default="WARNING")
LOG_QUERIES = config("LOG_QUERIES", default=False)
LOG_REQUESTS = config("LOG_REQUESTS", default=False)
if LOG_QUERIES and not DEBUG:
    warnings.warn(
        "Requested LOG_QUERIES=1 but DEBUG is false, no query logs will be emited.",
        RuntimeWarning,
    )

LOGGING_DIR = os.path.join(BASE_DIR, "log")

_root_handlers = ["console"] if LOG_STDOUT else ["project"]
_django_handlers = ["console"] if LOG_STDOUT else ["django"]

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
        "db": {"format": "%(asctime)s | %(message)s"},
        "outgoing_requests": {"()": HttpFormatter},
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "failed_notification": {
            "()": "openzaak.notifications.filters.FailedNotificationFilter"
        },
    },
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
        "console_db": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "db",
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
        "failed_notification": {
            "level": "DEBUG",
            "filters": ["failed_notification"],
            "class": "openzaak.notifications.handlers.DatabaseLogHandler",
        },
        "log_outgoing_requests": {
            "level": "DEBUG",
            "formatter": "outgoing_requests",
            "class": "logging.StreamHandler",  # to write to stdout
        },
        "save_outgoing_requests": {
            "level": "DEBUG",
            # enabling saving to database
            "class": "log_outgoing_requests.handlers.DatabaseOutgoingRequestsHandler",
        },
    },
    "loggers": {
        "": {"handlers": _root_handlers, "level": "ERROR", "propagate": False,},
        "openzaak": {
            "handlers": _root_handlers,
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "mozilla_django_oidc": {"handlers": _root_handlers, "level": LOG_LEVEL,},
        "openzaak.utils.middleware": {
            "handlers": _root_handlers,
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "vng_api_common": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["console_db"] if LOG_QUERIES else [],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": _django_handlers,
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.template": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "notifications_api_common.tasks": {
            "handlers": [
                "failed_notification",  # always log this to the database!
                *_root_handlers,
            ],
            "level": "WARNING",
            "propagate": True,
        },
        "log_outgoing_requests": {
            "handlers": ["log_outgoing_requests", "save_outgoing_requests"]
            if LOG_REQUESTS
            else [],
            "level": "DEBUG",
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
    "axes.backends.AxesBackend",
    "openzaak.accounts.backends.UserModelEmailBackend",
    "django.contrib.auth.backends.ModelBackend",
    "mozilla_django_oidc_db.backends.OIDCAuthenticationBackend",
]

SESSION_COOKIE_NAME = "openzaak_sessionid"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

LOGIN_URL = reverse_lazy("admin:login")
LOGIN_REDIRECT_URL = reverse_lazy("admin:index")
LOGOUT_REDIRECT_URL = reverse_lazy("admin:index")

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
SILENCED_SYSTEM_CHECKS = [
    "rest_framework.W001",
    "debug_toolbar.W006",
]


#
# Increase number of parameters for GET/POST requests
#
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

#
# Custom settings
#
PROJECT_NAME = "Open Zaak"
SITE_TITLE = "API dashboard"

# if specified, this replaces the host information in the requests, and it is used
# to build absolute URLs.
OPENZAAK_DOMAIN = config("OPENZAAK_DOMAIN", "")
OPENZAAK_REWRITE_HOST = config("OPENZAAK_REWRITE_HOST", False)

ENVIRONMENT = config("ENVIRONMENT", "")
ENVIRONMENT_SHOWN_IN_ADMIN = True

# settings for uploading large files
MIN_UPLOAD_SIZE = config("MIN_UPLOAD_SIZE", 4 * 2 ** 30)
# default to the MIN_UPLOAD_SIZE, as that is typically the maximum post body size configured
# in the webserver
DOCUMENTEN_UPLOAD_CHUNK_SIZE = config("DOCUMENTEN_UPLOAD_CHUNK_SIZE", MIN_UPLOAD_SIZE)
DOCUMENTEN_UPLOAD_READ_CHUNK = config(
    "DOCUMENTEN_UPLOAD_READ_CHUNK", 6 * 2 ** 20
)  # 6 MB default
DOCUMENTEN_UPLOAD_DEFAULT_EXTENSION = "bin"

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
    "autorisaties": os.path.join(
        BASE_DIR, "src", "openzaak", "components", "autorisaties", "openapi.yaml"
    ),
}

# Generating the schema, depending on the component
subpath = config("SUBPATH", None)
if subpath:
    if not subpath.startswith("/"):
        subpath = f"/{subpath}"
    SUBPATH = subpath

if "GIT_SHA" in os.environ:
    GIT_SHA = config("GIT_SHA", "")
# in docker (build) context, there is no .git directory
elif os.path.exists(os.path.join(BASE_DIR, ".git")):
    try:
        import git
    except ImportError:
        GIT_SHA = None
    else:
        repo = git.Repo(search_parent_directories=True)
        GIT_SHA = repo.head.object.hexsha
else:
    GIT_SHA = None

RELEASE = config("RELEASE", GIT_SHA)

NUM_PROXIES = config(  # TODO: this also is relevant for DRF settings if/when we have rate-limited endpoints
    "NUM_PROXIES", default=1, cast=lambda val: int(val) if val is not None else None,
)

##############################
#                            #
# 3RD PARTY LIBRARY SETTINGS #
#                            #
##############################

#
# DJANGO-AXES
#
AXES_CACHE = "axes"  # refers to CACHES setting
AXES_FAILURE_LIMIT = 5  # Default: 3
AXES_LOCK_OUT_AT_FAILURE = True  # Default: True
AXES_USE_USER_AGENT = False  # Default: False
AXES_COOLOFF_TIME = datetime.timedelta(minutes=5)
# after testing, the REMOTE_ADDR does not appear to be included with nginx (so single
# reverse proxy) and the ipware detection didn't properly work. On K8s you typically have
# ingress (load balancer) and then an additional nginx container for private file serving,
# bringing the total of reverse proxies to 2 - meaning HTTP_X_FORWARDED_FOR basically
# looks like ``$realIp,$ingressIp``. -> to get to $realIp, there is only 1 extra reverse
# proxy included.
AXES_PROXY_COUNT = NUM_PROXIES - 1 if NUM_PROXIES else None
AXES_ONLY_USER_FAILURES = (
    False  # Default: False (you might want to block on username rather than IP)
)
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = (
    False  # Default: False (you might want to block on username and IP)
)
# The default meta precedence order
IPWARE_META_PRECEDENCE_ORDER = (
    "HTTP_X_FORWARDED_FOR",
    "X_FORWARDED_FOR",  # <client>, <proxy1>, <proxy2>
    "HTTP_CLIENT_IP",
    "HTTP_X_REAL_IP",
    "HTTP_X_FORWARDED",
    "HTTP_X_CLUSTER_CLIENT_IP",
    "HTTP_FORWARDED_FOR",
    "HTTP_FORWARDED",
    "HTTP_VIA",
    "REMOTE_ADDR",
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
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=False)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", split=True, default=[])
CORS_ALLOWED_ORIGIN_REGEXES = config(
    "CORS_ALLOWED_ORIGIN_REGEXES", split=True, default=[]
)
# Authorization is included in default_cors_headers
CORS_ALLOW_HEADERS = (
    list(default_cors_headers)
    + ["accept-crs", "content-crs",]
    + config("CORS_EXTRA_ALLOW_HEADERS", split=True, default=[])
)
CORS_EXPOSE_HEADERS = [
    "content-crs",
]
# Django's SESSION_COOKIE_SAMESITE = "Lax" prevents session cookies from being sent
# cross-domain. There is no need for these cookies to be sent, since the API itself
# uses Bearer Authentication.
# we can't easily derive this from django-cors-headers, see also
# https://pypi.org/project/django-cors-headers/#csrf-integration
#
# So we do a best effort attempt at re-using configuration parameters, with an escape
# hatch to override it.
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    split=True,
    default=[strip_protocol_from_origin(origin) for origin in CORS_ALLOWED_ORIGINS],
)
#
# DJANGO-PRIVATES -- safely serve files after authorization
#
PRIVATE_MEDIA_ROOT = os.path.join(BASE_DIR, "private-media")
PRIVATE_MEDIA_URL = "/private-media/"

# requires an nginx container running in front
SENDFILE_BACKEND = config("SENDFILE_BACKEND", "django_sendfile.backends.nginx")
SENDFILE_ROOT = PRIVATE_MEDIA_ROOT
SENDFILE_URL = PRIVATE_MEDIA_URL

#
# ZGW-CONSUMERS
#
ZGW_CONSUMERS_TEST_SCHEMA_DIRS = [
    os.path.join(DJANGO_PROJECT_DIR, "tests", "schemas"),
    os.path.join(DJANGO_PROJECT_DIR, "selectielijst", "tests", "files"),
    os.path.join(DJANGO_PROJECT_DIR, "notifications", "tests", "files"),
]
ZGW_CONSUMERS_CLIENT_CLASS = "openzaak.client.OpenZaakClient"

#
# NOTIFICATIONS-API-COMMON
#
NOTIFICATIONS_DISABLED = config("NOTIFICATIONS_DISABLED", default=False)

#
# DJANGO-LOOSE-FK -- handle internal and external API resources
#
DEFAULT_LOOSE_FK_LOADER = "openzaak.loaders.AuthorizedRequestsLoader"

#
# RAVEN/SENTRY - error monitoring
#
SENTRY_DSN = config("SENTRY_DSN", None)

if SENTRY_DSN:
    SENTRY_CONFIG = {
        "dsn": SENTRY_DSN,
        "release": RELEASE or "RELEASE not set",
        "environment": ENVIRONMENT,
    }

    sentry_sdk.init(
        **SENTRY_CONFIG,
        integrations=get_sentry_integrations(),
        send_default_pii=True,
        before_send=filter_sensitive_data,
    )

#
# CELERY
#
CELERY_BROKER_URL = config("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")


#
# DJANGO-ADMIN-INDEX
#
ADMIN_INDEX_SHOW_REMAINING_APPS_TO_SUPERUSERS = False
ADMIN_INDEX_AUTO_CREATE_APP_GROUP = False

#
# Mozilla Django OIDC DB settings
#
OIDC_AUTHENTICATE_CLASS = "mozilla_django_oidc_db.views.OIDCAuthenticationRequestView"
MOZILLA_DJANGO_OIDC_DB_CACHE = "oidc"
MOZILLA_DJANGO_OIDC_DB_CACHE_TIMEOUT = 5 * 60

#
# Elastic APM
#
ELASTIC_APM_SERVER_URL = config("ELASTIC_APM_SERVER_URL", None)
ELASTIC_APM = {
    "SERVICE_NAME": f"Open Zaak - {ENVIRONMENT}",
    "SECRET_TOKEN": config("ELASTIC_APM_SECRET_TOKEN", "default"),
    "SERVER_URL": ELASTIC_APM_SERVER_URL,
}
if not ELASTIC_APM_SERVER_URL:
    ELASTIC_APM["ENABLED"] = False
    ELASTIC_APM["SERVER_URL"] = "http://localhost:8200"
else:
    MIDDLEWARE = ["elasticapm.contrib.django.middleware.TracingMiddleware"] + MIDDLEWARE
    INSTALLED_APPS = INSTALLED_APPS + [
        "elasticapm.contrib.django",
    ]


#
# LOG OUTGOING REQUESTS
#
LOG_OUTGOING_REQUESTS_DB_SAVE = config("LOG_OUTGOING_REQUESTS_DB_SAVE", default=False)


#
# Django setup configuration
#
SETUP_CONFIGURATION_STEPS = [
    "openzaak.config.bootstrap.site.SiteConfigurationStep",
    "openzaak.config.bootstrap.notifications.AuthNotificationStep",
    "openzaak.config.bootstrap.notifications.NotificationsAPIConfigurationStep",
    "openzaak.config.bootstrap.selectielijst.SelectielijstAPIConfigurationStep",
    "openzaak.config.bootstrap.demo.DemoUserStep",
]

#
# OpenZaak configuration
#


STORE_FAILED_NOTIFS = True

# Expiry time in seconds for JWT
JWT_EXPIRY = config("JWT_EXPIRY", default=3600)
# leeway when comparing timestamps - non-zero value account for clock drift
JWT_LEEWAY = config("JWT_LEEWAY", default=0)

CUSTOM_CLIENT_FETCHER = "openzaak.utils.auth.get_client"

CMIS_ENABLED = config("CMIS_ENABLED", default=False)
CMIS_MAPPER_FILE = config(
    "CMIS_MAPPER_FILE", default=os.path.join(BASE_DIR, "config", "cmis_mapper.json")
)
CMIS_URL_MAPPING_ENABLED = config("CMIS_URL_MAPPING_ENABLED", default=False)

# Name of the cache used to store responses for requests made when importing catalogi
IMPORT_REQUESTS_CACHE_NAME = config("IMPORT_REQUESTS_CACHE_NAME", "import_requests")

# Settings for setup_configuration command
# sites config
SITES_CONFIG_ENABLE = config("SITES_CONFIG_ENABLE", default=True)
OPENZAAK_ORGANIZATION = config("OPENZAAK_ORGANIZATION", "")
# notif -> OZ config
NOTIF_OPENZAAK_CONFIG_ENABLE = config("NOTIF_OPENZAAK_CONFIG_ENABLE", default=True)
NOTIF_OPENZAAK_CLIENT_ID = config("NOTIF_OPENZAAK_CLIENT_ID", "")
NOTIF_OPENZAAK_SECRET = config("NOTIF_OPENZAAK_SECRET", "")
# OZ -> notif config
OPENZAAK_NOTIF_CONFIG_ENABLE = config("OPENZAAK_NOTIF_CONFIG_ENABLE", default=True)
NOTIF_API_ROOT = config("NOTIF_API_ROOT", "")
if NOTIF_API_ROOT and not NOTIF_API_ROOT.endswith("/"):
    NOTIF_API_ROOT = f"{NOTIF_API_ROOT.strip()}/"
NOTIF_API_OAS = config("NOTIF_API_OAS", default=f"{NOTIF_API_ROOT}schema/openapi.yaml")
OPENZAAK_NOTIF_CLIENT_ID = config("OPENZAAK_NOTIF_CLIENT_ID", "")
OPENZAAK_NOTIF_SECRET = config("OPENZAAK_NOTIF_SECRET", "")
# Selectielijst config
OPENZAAK_SELECTIELIJST_CONFIG_ENABLE = config(
    "OPENZAAK_SELECTIELIJST_CONFIG_ENABLE", default=True
)
SELECTIELIJST_API_ROOT = config(
    "SELECTIELIJST_API_ROOT", default="https://selectielijst.openzaak.nl/api/v1/"
)
if SELECTIELIJST_API_ROOT and not SELECTIELIJST_API_ROOT.endswith("/"):
    SELECTIELIJST_API_ROOT = f"{SELECTIELIJST_API_ROOT.strip()}/"
SELECTIELIJST_API_OAS = config(
    "SELECTIELIJST_API_OAS", default=f"{SELECTIELIJST_API_ROOT}schema/openapi.yaml"
)
SELECTIELIJST_ALLOWED_YEARS = config(
    "SELECTIELIJST_ALLOWED_YEARS", default=[2017, 2020]
)
SELECTIELIJST_DEFAULT_YEAR = config("SELECTIELIJST_DEFAULT_YEAR", default=2020)
# Demo user config
DEMO_CONFIG_ENABLE = config("DEMO_CONFIG_ENABLE", default=DEBUG)
DEMO_CLIENT_ID = config("DEMO_CLIENT_ID", "")
DEMO_SECRET = config("DEMO_SECRET", "")
