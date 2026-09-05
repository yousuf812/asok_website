from django.contrib import admin

from .models import MembershipApplication


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):

    list_display = [
        "reference_number",
        "full_name",
        "email",
        "phone",
        "membership_type",
        "area_of_interest",
        "status",
        "created_at",
    ]

    list_filter = [
        "membership_type",
        "area_of_interest",
        "status",
        "created_at",
    ]

    search_fields = [
        "reference_number",
        "full_name",
        "email",
        "phone",
        "profession",
        "address",
        "motivation",
    ]

    list_editable = [
        "status",
    ]

    readonly_fields = [
        "reference_number",
        "created_at",
        "updated_at",
    ]

    date_hierarchy = "created_at"

    ordering = [
        "-created_at",
    ]

    fieldsets = (
        (
            "Application Information",
            {
                "fields": (
                    "reference_number",
                    "full_name",
                    "email",
                    "phone",
                    "membership_type",
                )
            },
        ),
        (
            "Background",
            {
                "fields": (
                    "profession",
                    "address",
                    "area_of_interest",
                    "motivation",
                )
            },
        ),
        (
            "Application Management",
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