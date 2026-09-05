from django.contrib import admin

from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = [
        "complaint_id",
        "subject",
        "category",
        "status",
        "is_anonymous",
        "created_at",
    ]

    list_filter = [
        "status",
        "category",
        "is_anonymous",
        "created_at",
    ]

    search_fields = [
        "complaint_id",
        "complainant_name",
        "email",
        "phone",
        "subject",
        "description",
        "location",
    ]

    list_editable = [
        "status",
    ]

    readonly_fields = [
        "complaint_id",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Complaint Information",
            {
                "fields": (
                    "complaint_id",
                    "complainant_name",
                    "email",
                    "phone",
                    "category",
                    "subject",
                    "incident_date",
                    "location",
                    "description",
                    "preferred_contact",
                    "is_anonymous",
                )
            },
        ),
        (
            "Case Management",
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

    ordering = [
        "-created_at"
    ]