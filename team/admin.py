from django.contrib import admin
from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "designation",
        "is_featured",
        "is_active",
        "order",
        "created_at",
    ]

    list_filter = [
        "designation",
        "is_featured",
        "is_active",
        "created_at",
    ]

    search_fields = [
        "name",
        "bio",
        "email",
        "phone",
    ]

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_editable = [
        "is_featured",
        "is_active",
        "order",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "designation",
                    "bio",
                    "photo",
                )
            },
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "phone",
                )
            },
        ),

        (
            "Social Links",
            {
                "fields": (
                    "facebook_url",
                    "linkedin_url",
                    "website_url",
                )
            },
        ),

        (
            "Display Settings",
            {
                "fields": (
                    "is_featured",
                    "is_active",
                    "order",
                )
            },
        ),

        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    ordering = [
        "order",
        "name",
    ]