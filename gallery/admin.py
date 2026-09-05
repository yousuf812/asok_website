from django.contrib import admin

from .models import GalleryCategory, GalleryImage


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "slug",
        "is_active",
        "order",
        "created_at",
    ]

    list_filter = [
        "is_active",
        "created_at",
    ]

    search_fields = [
        "name",
        "description",
    ]

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_editable = [
        "is_active",
        "order",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Category Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
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
        "name",
    ]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "category",
        "location",
        "taken_at",
        "is_featured",
        "is_active",
        "order",
    ]

    list_filter = [
        "category",
        "is_featured",
        "is_active",
        "taken_at",
    ]

    search_fields = [
        "title",
        "description",
        "location",
    ]

    prepopulated_fields = {
        "slug": ("title",)
    }

    autocomplete_fields = [
        "category",
    ]

    list_editable = [
        "is_featured",
        "is_active",
        "order",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    date_hierarchy = "taken_at"

    fieldsets = (
        (
            "Image Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "image",
                    "description",
                )
            },
        ),
        (
            "Event Details",
            {
                "fields": (
                    "location",
                    "taken_at",
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
        "-taken_at",
        "-created_at",
    ]