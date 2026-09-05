from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "is_active",
        "subscribed_at",
        "updated_at",
    ]

    list_filter = [
        "is_active",
        "subscribed_at",
    ]

    search_fields = [
        "email",
    ]

    list_editable = [
        "is_active",
    ]

    readonly_fields = [
        "subscribed_at",
        "updated_at",
    ]

    date_hierarchy = "subscribed_at"

    ordering = [
        "-subscribed_at",
    ]

    fieldsets = (
        (
            "Subscriber Information",
            {
                "fields": (
                    "email",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "subscribed_at",
                    "updated_at",
                )
            },
        ),
    )