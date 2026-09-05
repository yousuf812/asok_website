from django.contrib import admin
from .models import LegalAidRequest


@admin.register(LegalAidRequest)
class LegalAidRequestAdmin(admin.ModelAdmin):

    list_display = [
        "reference_number",
        "full_name",
        "category",
        "preferred_contact",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "category",
        "preferred_contact",
        "created_at",
    ]

    search_fields = [
        "reference_number",
        "full_name",
        "email",
        "phone",
        "subject",
        "description",
    ]

    list_editable = [
        "status",
    ]

    readonly_fields = [
        "reference_number",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Applicant Information",
            {
                "fields": (
                    "reference_number",
                    "full_name",
                    "email",
                    "phone",
                )
            },
        ),
        (
            "Request Details",
            {
                "fields": (
                    "category",
                    "subject",
                    "description",
                    "preferred_contact",
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

    ordering = ["-created_at"]