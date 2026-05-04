# jobs/admin.py
from django.contrib import admin
from .models import Company, Job, Application

# Basic registration
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)