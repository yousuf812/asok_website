from django.contrib import admin
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):

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


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "category",
        "author",
        "status",
        "is_featured",
        "published_at",
        "views",
    ]

    list_filter = [
        "status",
        "is_featured",
        "category",
        "published_at",
    ]

    search_fields = [
        "title",
        "excerpt",
        "content",
        "author",
    ]

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = [
        "status",
        "is_featured",
    ]

    readonly_fields = [
        "views",
        "created_at",
        "updated_at",
    ]

    autocomplete_fields = [
        "category",
    ]

    date_hierarchy = "published_at"

    fieldsets = (
        (
            "Post Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "excerpt",
                    "content",
                    "featured_image",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "author",
                    "status",
                    "is_featured",
                    "published_at",
                )
            },
        ),
        (
            "Statistics",
            {
                "fields": (
                    "views",
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
        "-published_at",
        "-created_at",
    ]