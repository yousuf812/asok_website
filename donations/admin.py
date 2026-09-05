from django.contrib import admin

from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):

    list_display = [
        "reference_number",
        "donor_name",
        "amount",
        "purpose",
        "payment_method",
        "transaction_id",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "payment_method",
        "purpose",
        "created_at",
    ]

    search_fields = [
        "reference_number",
        "donor_name",
        "email",
        "phone",
        "transaction_id",
        "message",
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
            "Donation Information",
            {
                "fields": (
                    "reference_number",
                    "donor_name",
                    "email",
                    "phone",
                    "amount",
                    "purpose",
                )
            },
        ),
        (
            "Payment Information",
            {
                "fields": (
                    "payment_method",
                    "transaction_id",
                    "status",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "message",
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