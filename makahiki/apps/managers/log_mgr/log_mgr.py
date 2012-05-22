"""log manager module provides methods to operate on log records."""
#import logging
import datetime
from apps.managers.log_mgr.models import MakahikiLog


def clear():
    """clear the log content from the log table."""
    MakahikiLog.objects.all().delete()


def write_log_entry(request, response=None, exception=None):
    """Write a log entry corresponding to the passed request."""

    log = MakahikiLog()

    # get the request header and response code into log record
    get_request_headers(log, request, response)

    # Create the log entry.
    #entry = "%s %s %s %s %s %d %s %s " % (
    #    log.request_time.strftime("%Y-%m-%d %H:%M:%S"), log.remote_ip, log.remote_user,
    #    log.request_method, log.request_url, log.response_status, log.http_referer,
    #    log.http_user_agent)

    #logger = logging.getLogger("makahiki_logger")

    if exception:
        log.post_content = "%s" % exception
        log.level = "ERROR"

        #entry += log.post_content
        #logger.error(entry)
    else:
        if request.FILES:
            # Append the filenames to the log.
            filenames = (f.name for f in request.FILES.values())
            file_str = "<Files: %s>" % " ".join(filenames)
            log.post_content = "%s" % (file_str,)
            #entry += log.post_content
        elif request.method == "POST":
            # Dump the POST parameters, but we don't need the CSRF token and password.
            query_dict = request.POST.copy()
            # print query_dict
            if u"csrfmiddlewaretoken" in query_dict:
                del query_dict[u'csrfmiddlewaretoken']
            if u"password" in query_dict:
                del query_dict[u'password']
            log.post_content = "%s" % (query_dict,)
            #entry += log.post_content

        log.level = "INFO"
        #logger.info(entry)

    log.save()


def get_request_headers(log, request, response):
    """returns a string consists of interesting request headers."""
    # Helper lambda for retrieving environment variables:
    header = lambda e, d: request.META[e] if e in request.META else d

    log.request_time = datetime.datetime.today()
    log.remote_ip = header("REMOTE_ADDR", "no-ip")
    log.remote_user = get_username(request)
    log.request_method = request.method
    log.request_url = request.get_full_path()
    log.response_status = response.status_code if response else 500
    log.http_referer = header("HTTP_REFERER", "no-referer")
    log.http_user_agent = header("HTTP_USER_AGENT", "no-user-agent")


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
