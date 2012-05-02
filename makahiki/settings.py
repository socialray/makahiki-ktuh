"""Djanjo settings file containing system-level settings.
   Settings include database, cache, path, middleware, and installed apps and logging."""

import posixpath
import os
import urlparse
import sys

###############
# PATH settings
###############
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ROOT_URLCONF = 'urls'

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
    ]

#######################
# static media settings
#######################
# serve media through django.views.static.serve.
SERVE_MEDIA = True

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'media')

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/site_media/media/'

# Absolute path to the directory that holds static files like app media.
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')

# URL that handles the static files like app media.
STATIC_URL = '/site_media/static/'

# directories which hold static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'media'),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a trailing slash.
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

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
    "apps.managers.challenge_mgr.context_processors.competition",
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
    'apps.lib.django_cas.middleware.CASMiddleware',

    'apps.managers.player_mgr.middleware.LoginMiddleware',
    'apps.managers.log_mgr.middleware.LoggingMiddleware',

    'django.middleware.cache.FetchFromCacheMiddleware',
    #always end with this for caching
    )

######################
# AUTH settings
######################
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.managers.auth_mgr.models.MakahikiCASBackend',
    )

AUTH_PROFILE_MODULE = 'player_mgr.Profile'

###################
# Authentication
###################
CAS_REDIRECT_URL = '/home'
CAS_IGNORE_REFERER = True

LOGIN_URL = "/account/cas/login/"
LOGIN_REDIRECT_URLNAME = "home_index"
LOGIN_REDIRECT_URL = "/home"
RESTRICTED_URL = '/restricted/'

#################
# CACHE settings
#################
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 600
MEMCACHED_CACHES = {'default':
                        {'BACKEND': 'django_pylibmc.memcached.PyLibMCCache'}}
DUMMY_CACHES = {'default':
                        {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}

#########################
# INSTALLED_APPS settings
#########################
INSTALLED_APPS = (
    # Makahiki pages
    'apps.template_support',
    'apps.pages',

    # Makahiki components
    'apps.managers.auth_mgr',
    'apps.managers.challenge_mgr',
    'apps.managers.team_mgr',
    'apps.managers.resource_mgr',
    'apps.managers.player_mgr',
    'apps.managers.score_mgr',
    'apps.managers.cache_mgr',

    # 3rd party libraries
    'apps.lib.django_cas',
    'apps.lib.brabeion',
    'apps.lib.facebook_api',
    'apps.lib.avatar',
    'gunicorn',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',

    # external
    'django_extensions',
    'django.contrib.staticfiles',

    # internal
    'django.contrib.admin',
    'django.contrib.markup',
)

################################
# INSTALLED Widgets
################################
INSTALLED_DEFAULT_WIDGET_APPS = (
    'quests',
    'notifications',
    'ask_admin',
    'home',
    'help',
)
for widget in INSTALLED_DEFAULT_WIDGET_APPS:
    INSTALLED_APPS += ("apps.widgets." + widget, )

################################
# INSTALLED Widgets
################################
INSTALLED_WIDGET_APPS = (
    'ask_admin',
    'badges',
    'canopy_viz',
    'canopy_member',
    'energy_goal',
    'energy_power_meter',
    'resource_scoreboard',
    'resource_scoreboard.energy',
    'resource_scoreboard.water',
    'my_achievements',
    'my_commitments',
    'my_info',
    'popular_tasks',
    'prizes',
    'quests',
    'raffle',
    'scoreboard',
    'smartgrid',
    'team_members',
    'upcoming_events',
    'wallpost',
    'help.intro',
    'help.faq',
    'help.rule',
    'status',
    'status.prizes',
    'status.rsvps',
    'status.users',
    'status.actions',
)

for widget in INSTALLED_WIDGET_APPS:
    INSTALLED_APPS += ("apps.widgets." + widget, )

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
# Default log file location.
LOG_FILE = 'makahiki.log'

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

#########################
# MISC
#########################

# Permissions for large uploaded files.
FILE_UPLOAD_PERMISSIONS = 0644

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Locale Info
TIME_ZONE = 'Pacific/Honolulu'
LOCALE_SETTING = 'en'
LANGUAGE_CODE = 'en_US.UTF-8'

# Markdown info
MARKDOWN_LINK = "http://daringfireball.net/projects/markdown/syntax"
MARKDOWN_TEXT = "Uses <a href=\"" + MARKDOWN_LINK + "\" target=\"_blank\">Markdown</a> formatting."


##############################
# Dummy setting for CHALLENGE
##############################
# set the dummpy challenge object to by pass reference check.
# It should be overridden from the DB ChallengeSettings object.
class Challenge():
    """Defines the dummy global settings for the challenge. """
    competition_name = None

CHALLENGE = Challenge()
COMPETITION_ROUNDS = None

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

# email Settings
if 'MAKAHIKI_EMAIL_INFO' in os.environ:
    email_info = os.environ['MAKAHIKI_EMAIL_INFO'].split(":")
    EMAIL_HOST_USER = email_info[0]
    EMAIL_HOST_PASSWORD = email_info[1]

# DEBUG settings
DEBUG = False
TEMPLATE_DEBUG = False
if 'MAKAHIKI_DEBUG' in os.environ and os.environ['MAKAHIKI_DEBUG'].lower() == "true":
    DEBUG = True
    TEMPLATE_DEBUG = True

# CACHE settings
if 'MAKAHIKI_MEMCACHED_ENABLED' in os.environ and\
   os.environ['MAKAHIKI_MEMCACHED_ENABLED'] == "True":
    CACHES = MEMCACHED_CACHES
else:
    CACHES = DUMMY_CACHES