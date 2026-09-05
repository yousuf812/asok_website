from django.contrib import admin

from .models import OrganizationInfo


@admin.register(OrganizationInfo)
class OrganizationInfoAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "updated_at",
    ]

    readonly_fields = [
        "updated_at",
    ]