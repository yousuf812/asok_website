from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = [
        "full_name",
        "email",
        "phone",
        "subject",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "created_at",
    ]

    search_fields = [
        "full_name",
        "email",
        "phone",
        "subject",
        "message",
    ]

    list_editable = [
        "status",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    date_hierarchy = "created_at"

    ordering = [
        "-created_at",
    ]

    fieldsets = (
        (
            "Contact Information",
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone",
                )
            },
        ),

        (
            "Message",
            {
                "fields": (
                    "subject",
                    "message",
                )
            },
        ),

        (
            "Message Management",
            {
                "fields": (
                    "status",
                    "admin_notes",
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