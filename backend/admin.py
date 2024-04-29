from django.contrib import admin

from django.contrib.auth import models
from django.contrib.admin.models import LogEntry

admin.site.site_header = "Nisira Admin"
admin.site.site_title = "Nisira Admin Portal"
admin.site.index_title = "Nisira BI"

admin.site.register(models.Permission)
admin.site.register(LogEntry)





