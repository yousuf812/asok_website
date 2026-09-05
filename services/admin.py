from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "icon",
        "is_active",
        "order",
        "created_at",
    ]

    list_filter = [
        "is_active",
        "icon",
        "created_at",
    ]

    search_fields = [
        "title",
        "description",
    ]

    prepopulated_fields = {
        "slug": ("title",)
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
        "-created_at",
    ]