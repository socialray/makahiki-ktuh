"""A middleware class to support logging of interactions with logged in users."""
import logging
import re
from time import strftime  # Timestamp


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

        # Retrieve the username either from a cookie (when logging out) or
        # the authenticated user.
        username = "not-login"
        if hasattr(request, "session") and "logged-out-user" in request.session:
            username = request.session["logged-out-user"]
            del request.session["logged-out-user"]
        elif hasattr(request, "user") and request.user.is_authenticated():
            username = request.user.username

        if username:
            # if request.session.get('staff', False):
            #   username = username + '*'
            self.__write_log_entry(username, request, response=response)

        return response



    def __write_log_entry(self, username, request, response=None):
        """Write a log entry corresponding to the passed request."""

        # Helper lambda for retrieving environment variables:
        header = lambda e, d: request.META[e] if e in request.META else d

        path = request.get_full_path()
        code = response.status_code if response else 500
        method = request.method
        ip_addr = header("REMOTE_ADDR", "no-ip")
        referer = header("HTTP_REFERER", "no-referer")
        user_agent = header("HTTP_USER_AGENT", "no-user-agent")

        timestamp = strftime("%Y-%m-%d %H:%M:%S")

        # Create the log entry.
        entry = "%s %s %s %s %s %d %s %s" % (
            timestamp, ip_addr, username, method, path, code, referer, user_agent)
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

        logger = logging.getLogger("makahiki_logger")
        logger.info(entry)
