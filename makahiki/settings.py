"""
 settings.py
 This file contains system level settings.
 Settings include database, cache, path, middleware, and installed apps and logging.
 New settings should not be added here.
"""

import os.path
import posixpath

##############
# DB settings
##############
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
        'USER': '',
        'PASSWORD': '',
        }
}

#######################
# Cache settings
#######################
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
# Note that this set up means the per site cache applies only to the landing and about pages.
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 600

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

# Location to save the files used for confirming activities (if enabled).
# Location is relative to MEDIA_ROOT.
ACTIVITY_FILE_DIR = "activities"

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

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
    }

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
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'lib.django_cas.middleware.CASMiddleware',
    'managers.player_mgr.middleware.LoginTrackingMiddleware',
    'managers.log_mgr.middleware.LoggingMiddleware',
    'pages.home.middleware.CompetitionMiddleware',
    'pages.home.middleware.CheckSetupMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    )

######################
# AUTH settings
######################
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'managers.auth_mgr.models.MakahikiCASBackend',
    )

#########################
# INSTALLED_APPS settings
#########################
INSTALLED_APPS = (
    # Makahiki pages
    'apps',
    'pages',
    'pages.home',

    # Makahiki components
    'managers.auth_mgr',
    'managers.settings_mgr',
    'managers.team_mgr',
    'managers.player_mgr',
    'managers.score_mgr',
    'managers.cache_mgr',
    'managers.help_mgr',

    'widgets.help_intro',
    'widgets.help_faq',
    'widgets.help_rule',
    'widgets.ask_admin',
    #'widgets.prizes',
    #'widgets.smartgrid',
    #'widgets.energy',
    #'widgets.quests',
    #'widgets.upcoming_events',
    #'widgets.badges',
    #'widgets.notifications',
    #'widgets.profile',
    #'widgets.news',
    #'widgets.canopy',
    #'widgets.analytics',

    # 3rd party libraries
    'lib.django_cas',
    'lib.brabeion',
    'lib.facebook_api',
    'lib.avatar',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.messages',

    # external
    'staticfiles',
    'django_nose',

    # internal
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',

    # migration support. comment out if module is not installed.
    'south',
    )

################
# TEST settings
################
# South
SOUTH_TESTS_MIGRATE = False

# Use Nose as the test runner.
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

################
# DEBUG settings
################
DEBUG = True
TEMPLATE_DEBUG = DEBUG
EMAIL_DEBUG = DEBUG

# serve media through django.views.static.serve.
SERVE_MEDIA = DEBUG

##########################
# MISC
#########################
EMAIL_CONFIRMATION_DAYS = 2

# Permissions for large uploaded files.
FILE_UPLOAD_PERMISSIONS = 0644

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

MARKUP_FILTER_FALLBACK = 'none'
MARKUP_CHOICES = (
    ('restructuredtext', u'reStructuredText'),
    ('textile', u'Textile'),
    ('markdown', u'Markdown'),
    ('creole', u'Creole'),
    )
WIKI_MARKUP_CHOICES = MARKUP_CHOICES

AUTH_PROFILE_MODULE = 'player_mgr.Profile'
# NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

# ACCOUNT_OPEN_SIGNUP is not used by this project, but it acts as if it was
# set to False
ACCOUNT_OPEN_SIGNUP = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False

################################
# Load additional settings files
################################
try:
    from game_settings import *  # pylint: disable=W0401,W0614
except ImportError:
    pass

try:
    from page_settings import *  # pylint: disable=W0401,W0614
except ImportError:
    pass

LOCAL_INSTALLED_APPS = ()
try:
    from local_settings import *  # pylint: disable=W0401,W0614, F0401
except ImportError:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS  # pylint: disable=E0602
except NameError:
    pass

##############################
# LOGGING settings
##############################
# Logging is defined down here to give local_settings a chance to override
# the default log file location.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
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
