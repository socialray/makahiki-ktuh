"""
url def for home page and setup wizard.
"""

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^restricted/$', 'widgets.home.views.restricted', name="home_restricted"),
    url(r'^setup/welcome/$', 'widgets.home.views.setup_welcome', name="setup_welcome"),
    url(r'^setup/terms/$', 'widgets.home.views.terms', name="setup_terms"),
    url(r'^setup/referral/$', 'widgets.home.views.referral', name='setup_referral'),
    url(r'^setup/profile/$', 'widgets.home.views.setup_profile', name="setup_profile"),
    url(r'^setup/profile/facebook/$', 'widgets.home.views.profile_facebook',
        name="setup_profile_facebook"),
    url(r'^setup/activity/$', 'widgets.home.views.setup_activity', name="setup_activity"),
    url(r'^setup/question/$', 'widgets.home.views.setup_question', name="setup_question"),
    url(r'^setup/complete/$', 'widgets.home.views.setup_complete', name="setup_complete"),
)
