"""Djanjo settings file containing system-level settings.
   Settings include database, cache, path, middleware, and installed apps and logging."""

import posixpath
import os
import urlparse
import sys

SITE_ID = 1

###############
# PATH settings
###############
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Default log file location.
LOG_FILE = 'makahiki.log'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'media')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/site_media/media/'

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = '/site_media/static/'

# Additional directories which hold static files
STATICFILES_DIRS = (
    ('makahiki', os.path.join(PROJECT_ROOT, 'media')),
    )

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

ROOT_URLCONF = 'urls'

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
    ]

#######################
# Template settings
#######################
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(PROJECT_ROOT, "apps"),
    )

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.contrib.messages.context_processors.messages',
    "managers.settings_mgr.context_processors.competition",
    )

######################
# MIDDLEWARE settings
######################
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    #always start with this for caching

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'lib.django_cas.middleware.CASMiddleware',

    'managers.player_mgr.middleware.LoginMiddleware',
    'managers.log_mgr.middleware.LoggingMiddleware',

    'django.middleware.cache.FetchFromCacheMiddleware',
    #always end with this for caching
    )

######################
# AUTH settings
######################
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'managers.auth_mgr.models.MakahikiCASBackend',
    )

AUTH_PROFILE_MODULE = 'player_mgr.Profile'

###################
# Authentication
###################
CAS_REDIRECT_URL = '/home'
CAS_IGNORE_REFERER = True

LOGIN_URL = "/account/cas/login/"
LOGIN_REDIRECT_URLNAME = "home_index"
LOGIN_REDIRECT_URL = "/"
RESTRICTED_URL = '/restricted/'

#########################
# INSTALLED_APPS settings
#########################
INSTALLED_APPS = (
    # Makahiki pages
    'apps',
    'pages',

    # Makahiki components
    'managers.auth_mgr',
    'managers.settings_mgr',
    'managers.team_mgr',
    'managers.player_mgr',
    'managers.score_mgr',
    'managers.cache_mgr',
    'managers.help_mgr',

    # 3rd party libraries
    'lib.django_cas',
    'lib.brabeion',
    'lib.facebook_api',
    'lib.avatar',
    'gunicorn',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.messages',

    # external
    'staticfiles',
    'django_extensions',

    # internal
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
)

################################
# INSTALLED Widgets
################################
INSTALLED_WIDGET_APPS = (
    'widgets.ask_admin',
    'widgets.badges',
    'widgets.energy_goal',
    'widgets.energy_power_meter',
    'widgets.energy_scoreboard',
    'widgets.help_faq',
    'widgets.help_intro',
    'widgets.help_rule',
    'widgets.home',
    'widgets.my_achievements',
    'widgets.my_commitments',
    'widgets.my_info',
    'widgets.notifications',
    'widgets.popular_tasks',
    'widgets.prizes',
    'widgets.quests',
    'widgets.raffle',
    'widgets.scoreboard',
    'widgets.smartgrid',
    'widgets.team_members',
    'widgets.upcoming_events',
    'widgets.wallpost',
)

INSTALLED_APPS += INSTALLED_WIDGET_APPS

# migration support, need to be the last app.
# nose has to be after south!
INSTALLED_APPS += ('south', 'django_nose',)

################
# TEST settings
################
# South
SOUTH_TESTS_MIGRATE = False

# Use Nose as the test runner.
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

##############################
# LOGGING settings
##############################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %'
                      '(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
            },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'simple',
            }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
            },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            },
        'makahiki_logger': {
            'handlers': ['file'],
            'level': 'INFO',
            }
    }
}

##########################
# MISC
#########################
# serve media through django.views.static.serve.
SERVE_MEDIA = True

EMAIL_CONFIRMATION_DAYS = 2

# Permissions for large uploaded files.
FILE_UPLOAD_PERMISSIONS = 0644

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

#############################################
# Load sensitive settings from OS environment
#############################################
# DB settings
if 'DATABASE_URL' in os.environ:
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    if url.scheme == 'postgres':
        DATABASES = {}
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
            }
else:
    if 'READTHEDOCS' not in os.environ:
        print "Environment variable DATABASE_URL not defined. Exiting."
        sys.exit(1)

# Admin info Settings
if 'MAKAHIKI_ADMIN_INFO' in os.environ:
    admin_info = os.environ['MAKAHIKI_ADMIN_INFO'].split(":")
    ADMIN_USER = admin_info[0]
    ADMIN_PASSWORD = admin_info[1]
else:
    if 'READTHEDOCS' not in os.environ:
        print "Environment variable MAKAHIKI_ADMIN_INFO not defined. Exiting."
        sys.exit(1)

# DEBUG settings
DEBUG = True
TEMPLATE_DEBUG = True
if 'MAKAHIKI_HEROKU' in os.environ and os.environ['MAKAHIKI_HEROKU'] == "True":
    DEBUG = False
    TEMPLATE_DEBUG = False

# CACHE settings
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 600
if 'MAKAHIKI_HEROKU' in os.environ and os.environ['MAKAHIKI_HEROKU'] == "True":
    CACHES = {
        'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache'
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
    }
