from django.contrib import admin

from . import models


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author_names")

    @admin.display(description="Authors")  # type: ignore[attr-defined]
    def author_names(self, obj):
        return ", ".join(author.name for author in obj.authors.all())
