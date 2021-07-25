from django.contrib import admin

from . import models


@admin.register(models.Volume)
class VolumeAdmin(admin.ModelAdmin):
    pass
