from django.contrib import admin
from . import models

admin.site.register(models.Organization)
admin.site.register(models.BoardMember)
