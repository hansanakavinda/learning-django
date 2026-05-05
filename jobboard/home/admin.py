# home/admin.py
from django.contrib import admin
from .models import Question, Choice

# Basic registration
admin.site.register(Question)
admin.site.register(Choice)