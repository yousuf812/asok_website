from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "published_date",
        "is_active",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "is_active",
        "published_date",
        "created_at",
    ]

    search_fields = [
        "title",
        "description",
    ]

    list_editable = [
        "is_active",
    ]

    readonly_fields = [
        "slug",
        "created_at",
        "updated_at",
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    date_hierarchy = "published_date"

    ordering = [
        "-published_date",
        "-created_at",
    ]

    fieldsets = (
        (
            "Project Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "image",
                    "description",
                )
            },
        ),
        (
            "Publication",
            {
                "fields": (
                    "published_date",
                    "is_active",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )