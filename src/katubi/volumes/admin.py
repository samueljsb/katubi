from django.contrib import admin
from django.utils.html import format_html

from . import models


@admin.register(models.Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ("cover_image", "book", "isbn")
    list_display_links = ("cover_image", "book")
    list_select_related = ("book",)

    @admin.display(description="Cover")  # type: ignore[attr-defined]
    def cover_image(self, obj):
        return format_html(
            f'<img src="{obj.cover_image_url}" style="max-height:100px;"/>'
        )
