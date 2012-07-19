"""models to store log records."""
from django.db import models


class MakahikiLog(models.Model):
    """a simple log record table."""
    level = models.CharField(max_length=10, blank=True, null=True)
    request_time = models.DateTimeField(blank=True, null=True)
    remote_ip = models.CharField(max_length=20, blank=True, null=True)
    remote_user = models.CharField(max_length=30, blank=True, null=True, db_index=True)
    request_method = models.CharField(max_length=10, blank=True, null=True)
    request_url = models.CharField(max_length=1000, blank=True, null=True)
    response_status = models.IntegerField(blank=True, null=True)
    http_referer = models.CharField(max_length=1000, blank=True, null=True)
    http_user_agent = models.CharField(max_length=300, blank=True, null=True)
    post_content = models.TextField(blank=True, null=True)
