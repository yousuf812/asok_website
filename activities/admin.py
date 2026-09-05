from django.contrib import admin
from .models import Activity, ImpactStatistic


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "category",
        "status",
        "location",
        "beneficiaries",
        "is_featured",
        "is_active",
        "order",
        "start_date",
    ]

    list_filter = [
        "category",
        "status",
        "is_featured",
        "is_active",
        "start_date",
    ]

    search_fields = [
        "title",
        "short_description",
        "description",
        "location",
    ]

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = [
        "status",
        "is_featured",
        "is_active",
        "order",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    date_hierarchy = "start_date"

    fieldsets = (
        (
            "Activity Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "short_description",
                    "description",
                    "image",
                )
            },
        ),

        (
            "Project Details",
            {
                "fields": (
                    "location",
                    "start_date",
                    "end_date",
                    "beneficiaries",
                    "status",
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
        "-start_date",
        "-created_at",
    ]


@admin.register(ImpactStatistic)
class ImpactStatisticAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "value",
        "suffix",
        "is_active",
        "order",
        "updated_at",
    ]

    list_filter = [
        "is_active",
    ]

    search_fields = [
        "title",
        "description",
    ]

    list_editable = [
        "value",
        "suffix",
        "is_active",
        "order",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Statistic Information",
            {
                "fields": (
                    "title",
                    "value",
                    "suffix",
                    "description",
                    "icon",
                )
            },
        ),
        (
            "Display Settings",
            {
                "fields": (
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
        "id",
    ]