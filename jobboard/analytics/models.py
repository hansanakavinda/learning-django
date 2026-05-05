# analytics/models.py

from django.db import models


class Report(models.Model):
    """This will live in SQLite."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MetricLog(models.Model):
    """This will live in Neon PostgreSQL."""

    event_name = models.CharField(max_length=200)
    value = models.FloatField()
    metadata = models.JSONField(default=dict, blank=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name}: {self.value}"