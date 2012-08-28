"""A middleware class to support logging of interactions with logged in users."""
import traceback
#import datetime
from django.core.signals import got_request_exception
from django.dispatch.dispatcher import receiver
import re


# Filter out requests to media and site_media.
from apps.managers.log_mgr import log_mgr

MEDIA_REGEXP = r'^\/site_media'
URL_FILTER = ("/favicon.ico", "/admin/jsi18n/")


class LoggingMiddleware(object):
    """Provides logging of logged in user interactions."""
    def process_response(self, request, response):
        """Log the actions of logged in users."""

        #time_start = datetime.datetime.now()

        # Filter out the following paths.  Logs will not be created for these
        # paths.
        if re.match(MEDIA_REGEXP, request.path) or \
           request.path in URL_FILTER:
            return response

        log_mgr.write_log_entry(request=request, response_status_code=response.status_code)

        #time_end = datetime.datetime.now()
        #print "%s time: %s" % ("logging", (time_end - time_start))
        #print "%s timestamp: %s" % ("End logging middleware", time_end)
        return response


@receiver(got_request_exception)
def log_request_exception(sender, **kwargs):
    """log the exception with traceback."""

    _ = sender
    exception = traceback.format_exc()
    request = kwargs["request"]
    log_mgr.write_log_entry(request=request, response_status_code=500, exception=exception)
