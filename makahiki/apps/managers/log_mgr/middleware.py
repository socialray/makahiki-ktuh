"""A middleware class to support logging of interactions with logged in users."""
import logging
import traceback
from django.core.signals import got_request_exception
from django.dispatch.dispatcher import receiver
import re
from time import strftime


# Filter out requests to media and site_media.
MEDIA_REGEXP = r'^\/(site_)?media'
SENTRY_REGEXP = r'^\/sentry\/'
URL_FILTER = ("/favicon.ico", "/admin/jsi18n/")


class LoggingMiddleware(object):
    """Provides logging of logged in user interactions."""
    def process_response(self, request, response):
        """Log the actions of logged in users."""

        # Filter out the following paths.  Logs will not be created for these
        # paths.
        if re.match(MEDIA_REGEXP, request.path) or re.match(SENTRY_REGEXP,
            request.path) or request.path in URL_FILTER:
            return response

        self.write_log_entry(request=request, response=response)

        return response

    @staticmethod
    def get_username(request):
        """Returns the username from request."""
        # Retrieve the username either from a cookie (when logging out) or
        # the authenticated user.
        username = "not-login"
        if hasattr(request, "session") and "logged-out-user" in request.session:
            username = request.session["logged-out-user"]
            del request.session["logged-out-user"]
        elif hasattr(request, "user") and request.user.is_authenticated():
            username = request.user.username
        return username

    @staticmethod
    def get_request_headers(request, response):
        """returns a string consists of interesting request headers."""
        # Helper lambda for retrieving environment variables:
        header = lambda e, d: request.META[e] if e in request.META else d

        path = request.get_full_path()
        code = response.status_code if response else 500
        method = request.method
        ip_addr = header("REMOTE_ADDR", "no-ip")
        referer = header("HTTP_REFERER", "no-referer")
        user_agent = header("HTTP_USER_AGENT", "no-user-agent")

        timestamp = strftime("%Y-%m-%d %H:%M:%S")

        username = LoggingMiddleware.get_username(request)

        # Create the log entry.
        entry = "%s %s %s %s %s %d %s %s" % (
            timestamp, ip_addr, username, method, path, code, referer, user_agent)

        return entry

    @staticmethod
    def write_log_entry(request, response=None, exception=None):
        """Write a log entry corresponding to the passed request."""

        logger = logging.getLogger("makahiki_logger")
        entry = LoggingMiddleware.get_request_headers(request, response)

        if exception:
            entry += " %s" % exception
            logger.error(entry)
        else:
            if request.method == "POST":
                # Dump the POST parameters, but we don't need the CSRF token.
                query_dict = request.POST.copy()
                # print query_dict
                if u"csrfmiddlewaretoken" in query_dict:
                    del query_dict[u'csrfmiddlewaretoken']
                if u"password" in query_dict:
                    del query_dict[u'password']

                entry += " %s" % (query_dict,)

            if request.FILES:
                # Append the filenames to the log.
                filenames = (f.name for f in request.FILES.values())
                file_str = "<Files: %s>" % " ".join(filenames)
                entry += " %s" % (file_str,)
            logger.info(entry)


@receiver(got_request_exception)
def log_request_exception(sender, **kwargs):
    """log the exception with traceback."""

    _ = sender
    exception = traceback.format_exc()
    request = kwargs["request"]
    LoggingMiddleware.write_log_entry(request=request, exception=exception)
