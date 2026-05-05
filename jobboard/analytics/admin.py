# home/admin.py
from django.contrib import admin
from .models import Report, MetricLog

# Basic registration
admin.site.register(Report)
admin.site.register(MetricLog)