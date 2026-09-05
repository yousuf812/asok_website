from django.contrib import admin

from .models import (
    HumanRightsCategory,
    HumanRightsArticle,
    HumanRightsFAQ,
)


@admin.register(HumanRightsCategory)
class HumanRightsCategoryAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "is_active",
        "order",
        "created_at",
    ]

    list_filter = [
        "is_active",
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

    ordering = [
        "order",
        "name",
    ]


@admin.register(HumanRightsArticle)
class HumanRightsArticleAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "category",
        "is_featured",
        "is_active",
        "order",
        "created_at",
    ]

    list_filter = [
        "category",
        "is_featured",
        "is_active",
        "created_at",
    ]

    search_fields = [
        "title",
        "short_description",
        "content",
    ]

    prepopulated_fields = {
        "slug": ("title",)
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

    autocomplete_fields = [
        "category",
    ]

    ordering = [
        "order",
        "-created_at",
    ]


@admin.register(HumanRightsFAQ)
class HumanRightsFAQAdmin(admin.ModelAdmin):

    list_display = [
        "question",
        "is_active",
        "order",
        "created_at",
    ]

    list_filter = [
        "is_active",
        "created_at",
    ]

    search_fields = [
        "question",
        "answer",
    ]

    list_editable = [
        "is_active",
        "order",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    ordering = [
        "order",
        "-created_at",
    ]