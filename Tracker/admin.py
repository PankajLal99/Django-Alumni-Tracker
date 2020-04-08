from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.Scrapper_Data)
admin.site.register(models.Blog)