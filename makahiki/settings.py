"""Provides system-level settings and access to environment variables.
All variables corresponding to environment variables have documentation for ReadTheDocs."""

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

# directories which hold static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
    )

# URL that handles the static files such as css, img, and js
STATIC_URL = "/site_media/static/"

# Absolute path to the directory that holds static files.
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')

# prefix for all uploaded media files
MAKAHIKI_MEDIA_PREFIX = "media"

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
    "django.core.context_processors.static",
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
    'apps.managers.auth_mgr.cas_backend.MakahikiCASBackend',
    #'apps.managers.auth_mgr.ldap_backend.MakahikiLDAPBackend',
    )

AUTH_PROFILE_MODULE = 'player_mgr.Profile'

###################
# Authentication
###################
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
    'apps.managers.log_mgr',
    'apps.test_helpers',

    # 3rd party libraries
    'apps.lib.django_cas',
    'apps.lib.brabeion',
    'apps.lib.facebook_api',
    'apps.lib.avatar',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.markup',

    # external
    'django_extensions',
    'gunicorn',
    'storages',
)

################################
# INSTALLED DEFAULT Widgets for all pages
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
    'resource_goal',
    'resource_goal.energy',
    'resource_goal.water',
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
    'logging',
)

for widget in INSTALLED_WIDGET_APPS:
    INSTALLED_APPS += ("apps.widgets." + widget, )

# migration support, need to be the last app.
# nose has to be after south!
INSTALLED_APPS += ('south', 'django_nose',)

################
# ADMIN APPS
################
ADMIN_APPS = (
    ("Challenge", ({"name": "Challenge settings", "url": "challenge_mgr/challengesettings"},
                   {"name": "Round settings", "url": "challenge_mgr/roundsettings"},
                   {"name": "Page info", "url": "challenge_mgr/pageinfo"},
                   {"name": "Score settings", "url": "score_mgr/scoresettings"})),
    ("Player", ({"name": "Groups", "url": "team_mgr/group"},
                   {"name": "Teams", "url": "team_mgr/team"},
                   {"name": "Users", "url": "auth/user"},
                   {"name": "Profiles", "url": "player_mgr/profile"},
                   {"name": "Team Posts", "url": "team_mgr/post"})),
    ("Resource", ({"name": "Energy goal settings", "url": "resource_goal/energygoalsetting"},
                   {"name": "Energy usages", "url": "resource_mgr/energyusage"},
                   {"name": "Water goal settings", "url": "resource_goal/watergoalsetting"},
                   {"name": "Water usages", "url": "resource_mgr/waterusage"})),
    ("Smartgrid", ({"name": "Levels", "url": "smartgrid/level"},
                   {"name": "Categories", "url": "smartgrid/category"},
                   {"name": "Activities", "url": "smartgrid/activity"},
                   {"name": "Commitments", "url": "smartgrid/commitment"},
                   {"name": "Events", "url": "smartgrid/event"},
                   {"name": "Action members", "url": "smartgrid/actionmember"})),
    ("Prize", ({"name": "Challenge Prizes", "url": "prizes/prize"},
                   {"name": "Raffle Prizes", "url": "raffle/raffleprize"})),
    ("Misc", ({"name": "Helps", "url": "help/helptopic"},
                   {"name": "Quests", "url": "quests/quest"},
                   {"name": "Makahiki logs", "url": "log_mgr/makahikilog"})),
    )

##########################################################
# INSTALLED Themes. Please keep them in alphabetical order
##########################################################
INSTALLED_THEMES = (
    'theme-bubbles',
    'theme-bumblebee',
    'theme-forest',
    'theme-google',
    'theme-sonora',
    'theme-space',
    'theme-wave',
)


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

SERIALIZATION_MODULES = {
    'csv': 'snippetscream.csv_serializer',
    }


##############################
# Dummy settings for CHALLENGE
##############################
# Create a dummy challenge object and variables so that IDEs are OK.
# This object will be instantiated for real from the DB ChallengeSettings object.
class Challenge():
    "Encapsulates settings for the challenge."
    competition_name = None

CHALLENGE = Challenge()
COMPETITION_ROUNDS = None

##################################################################################################
# Load environment variables
# Note: All environment variables have a corresponding Python variable for documentation purposes.
##################################################################################################

# Helper lambda for retrieving environment variables:
env = lambda e, d: os.environ[e] if e in os.environ else d

# DB settings
MAKAHIKI_USE_HEROKU = env('MAKAHIKI_USE_HEROKU', '').lower() == "true"
"""[Optional] If "true", use Heroku hosting, Otherwise, use local hosting."""

MAKAHIKI_DATABASE_URL = env('MAKAHIKI_DATABASE_URL', '')
"""[Required if MAKAHIKI_USE_HEROKU is not true] Specify the Database URL.
Example: postgres://username:password@db_host:db_port/db_name"""

if not MAKAHIKI_USE_HEROKU:
    if MAKAHIKI_DATABASE_URL:
        urlparse.uses_netloc.append('postgres')
        url = urlparse.urlparse(MAKAHIKI_DATABASE_URL)
        if url.scheme == 'postgres':
            DATABASES = {'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': url.path[1:],
                'USER': url.username,
                'PASSWORD': url.password,
                'HOST': url.hostname,
                'PORT': url.port,
                }}
    else:
        if 'READTHEDOCS' not in os.environ:
            print "Environment variable MAKAHIKI_DATABASE_URL not defined. Exiting."
            sys.exit(1)

# Admin info Settings
MAKAHIKI_ADMIN_INFO = env('MAKAHIKI_ADMIN_INFO', '')
"""[Required]  Specify the makahiki admin account and password.
Example:  admin:changeme"""
if MAKAHIKI_ADMIN_INFO:
    admin_info = MAKAHIKI_ADMIN_INFO.split(":")
    ADMIN_USER = admin_info[0]
    ADMIN_PASSWORD = admin_info[1]
else:
    if 'READTHEDOCS' not in os.environ:
        print "Environment variable MAKAHIKI_ADMIN_INFO not defined. Exiting."
        sys.exit(1)

# email Settings
MAKAHIKI_EMAIL_INFO = env('MAKAHIKI_EMAIL_INFO', '')
"""[Required if enabling email]  Specify the email host user and password.
Example:  kukuicup@gmail.com:changeme"""
if MAKAHIKI_EMAIL_INFO:
    email_info = MAKAHIKI_EMAIL_INFO.split(":")
    EMAIL_HOST_USER = email_info[0]
    EMAIL_HOST_PASSWORD = email_info[1]

# DEBUG settings
MAKAHIKI_DEBUG = env('MAKAHIKI_DEBUG', '').lower() == "true"
"""[Optional]  If "true", enable debug mode, with better error messages.
Otherwise use production mode."""
DEBUG = MAKAHIKI_DEBUG
TEMPLATE_DEBUG = MAKAHIKI_DEBUG

# CACHE settings
MAKAHIKI_USE_MEMCACHED = env('MAKAHIKI_USE_MEMCACHED', '').lower() == "true"
"""[Optional] If "true", use memcache. Otherwise no caching is used."""
if MAKAHIKI_USE_MEMCACHED:
    CACHES = {'default':
                {'BACKEND': 'django_pylibmc.memcached.PyLibMCCache'}}
else:
    CACHES = {'default':
                {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}

# static media settings
MAKAHIKI_USE_S3 = env('MAKAHIKI_USE_S3', '').lower() == "true"
"""[Optional] If "true", use the Amazon S3 storage facility. Otherwise use local folder."""

MAKAHIKI_AWS_ACCESS_KEY_ID = env('MAKAHIKI_AWS_ACCESS_KEY_ID', '')
"""[Required if MAKAHIKI_USE_S3 is true]  The Amazon access key ID."""
MAKAHIKI_AWS_SECRET_ACCESS_KEY = env('MAKAHIKI_AWS_SECRET_ACCESS_KEY', '')
"""[Required if MAKAHIKI_USE_S3 is true]  The Amazon secret access key."""
MAKAHIKI_AWS_STORAGE_BUCKET_NAME = env('MAKAHIKI_AWS_STORAGE_BUCKET_NAME', '')
"""[Required if MAKAHIKI_USE_S3 is true]  The Amazon storage bucket name."""

if MAKAHIKI_USE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    #STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
    AWS_ACCESS_KEY_ID = MAKAHIKI_AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = MAKAHIKI_AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = MAKAHIKI_AWS_STORAGE_BUCKET_NAME

    MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    SERVE_MEDIA = False
else:
    # URL that handles the media files such as uploads.
    MEDIA_URL = "/site_media/"
    # Absolute path to the directory that holds media.
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media')
    # serve media through django.views.static.serve.
    SERVE_MEDIA = True

# settings to use less files
MAKAHIKI_USE_LESS = env('MAKAHIKI_USE_LESS', '').lower() == "true"
"""[Optional] If "true", use LESS files to style pages. Otherwise use the latest version of CSS."""

# LDAP settings
MAKAHIKI_LDAP_BIND_DN = env('MAKAHIKI_LDAP_BIND_DN', '')
"""[Required for LDAP services] Provide the Bind domain name."""
AUTH_LDAP_BIND_DN = MAKAHIKI_LDAP_BIND_DN

MAKAHIKI_LDAP_BIND_PASSWORD = env('MAKAHIKI_LDAP_BIND_PWD', '')
"""[Required for LDAP services] Provide the Bind password."""
AUTH_LDAP_BIND_PASSWORD = MAKAHIKI_LDAP_BIND_PASSWORD

MAKAHIKI_SECRET_KEY = env('MAKAHIKI_SECRET_KEY', '')
"""[Optional] Specifies the Django secret key setting.
See https://docs.djangoproject.com/en/dev/ref/settings/#secret-key"""
SECRET_KEY = MAKAHIKI_SECRET_KEY

MAKAHIKI_USE_FACEBOOK = env('MAKAHIKI_USE_FACEBOOK', '').lower() == "true"
"""[Optional] If "true", use facebook integration."""
MAKAHIKI_FACEBOOK_APP_ID = env('MAKAHIKI_FACEBOOK_APP_ID', '')
"""[Required if using Facebook] App ID required for Facebook integration."""
MAKAHIKI_FACEBOOK_SECRET_KEY = env('MAKAHIKI_FACEBOOK_SECRET_KEY', '')
"""[Required if using Facebook] Secret key required for Facebook integration."""
if MAKAHIKI_USE_FACEBOOK:
    if not MAKAHIKI_FACEBOOK_APP_ID:
        print "Environment variable MAKAHIKI_FACEBOOK_APP_ID not defined. Exiting."
        sys.exit(1)
    if not MAKAHIKI_FACEBOOK_SECRET_KEY:
        print "Environment variable MAKAHIKI_FACEBOOK_SECRET_KEY not defined. Exiting."
        sys.exit(1)

MAKAHIKI_USE_LOGFILE = env('MAKAHIKI_USE_LOGFILE', '').lower() == "true"
"""[Optional] if "true", use logfile to store application logs."""
if MAKAHIKI_USE_LOGFILE:
    # Default log file location.
    LOG_FILE = 'makahiki.log'
    LOGGING['loggers']['makahiki_logger'] = {
        'handlers': ['file'],
        'level': 'INFO',
        }
    LOGGING['handlers']['file'] = {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename': LOG_FILE,
        'formatter': 'simple',
        }
