from django.contrib import admin

from . import models


@admin.register(models.ReadingEvent)
class ReadingEventAdmin(admin.ModelAdmin):
    date_hierarchy = "occurred_date"
    list_display = ("occurred_date", "user", "event_type", "book")
