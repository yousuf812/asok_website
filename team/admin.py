from django.contrib import admin
from django.core.exceptions import ValidationError

from membership.models import Member

from .forms import CommitteeMemberAdminForm
from .models import (
    TeamMember,
    CommitteeMember,
    CommitteeMinimum,
    Division,
    District,
    Upazila,
    Municipality,
    UnionWard,
)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "designation",
        "is_featured",
        "is_active",
        "order",
        "created_at",
    ]

    list_filter = [
        "designation",
        "is_featured",
        "is_active",
        "created_at",
    ]

    search_fields = [
        "name",
        "bio",
        "email",
        "phone",
    ]

    prepopulated_fields = {
        "slug": ("name",),
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

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "designation",
                    "bio",
                    "photo",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "phone",
                )
            },
        ),
        (
            "Social Links",
            {
                "fields": (
                    "facebook_url",
                    "linkedin_url",
                    "website_url",
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
        "name",
    ]


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):

    form = CommitteeMemberAdminForm

    class Media:
        js = (
            "team/js/committee_location.js",
        )

    list_display = [
        "member_id_display",
        "member_name",
        "committee_type",
        "member_type",
        "designation",
        "committee_member_count",
        "committee_minimum_required",
        "committee_status",
        "effective_date",
        "is_active",
    ]

    list_filter = [
        "committee_type",
        "member_type",
        "designation",
        "division",
        "district",
        "thana_upazila",
        "municipality",
        "union_ward",
        "is_active",
    ]

    search_fields = [
         "member__member_id",
         "member__application__full_name",
         "designation",
         "division__name",
         "district__name",
         "thana_upazila__name",
         "municipality__name",
         "union_ward__name",
         "village",
         "post_office",
    ]

    list_editable = [
        "is_active",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    autocomplete_fields = [
        "member",
    ]

    date_hierarchy = "effective_date"

    fieldsets = (
        (
            "Member & Committee",
            {
                "fields": (
                    "member",
                    "committee_type",
                    "member_type",
                    "designation",
                    "effective_date",
                    "is_active",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "division",
                    "district",
                    "thana_upazila",
                    "municipality",
                    "union_ward",
                    "village",
                    "post_office",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "notes",
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
        "committee_type",
        "designation",
        "member__application__full_name",
    ]

    def committee_member_count(self, obj):
        queryset = CommitteeMember.objects.filter(
            committee_type=obj.committee_type,
            is_active=True,
        )

        if obj.committee_type != "central":
            if obj.division_id:
                queryset = queryset.filter(
                    division_id=obj.division_id
                )

            if obj.district_id:
                queryset = queryset.filter(
                    district_id=obj.district_id
                )

            if obj.thana_upazila_id:
                queryset = queryset.filter(
                    thana_upazila_id=obj.thana_upazila_id
                )

            if obj.municipality_id:
                queryset = queryset.filter(
                    municipality_id=obj.municipality_id
                )

            if obj.union_ward_id:
                queryset = queryset.filter(
                    union_ward_id=obj.union_ward_id
                )

        return queryset.count()

    committee_member_count.short_description = "Active Members"

    def committee_minimum_required(self, obj):
        requirement = CommitteeMinimum.objects.filter(
            committee_type=obj.committee_type
        ).first()

        if requirement:
            return requirement.minimum_members

        return 0

    committee_minimum_required.short_description = "Minimum"

    def committee_status(self, obj):
        requirement = CommitteeMinimum.objects.filter(
            committee_type=obj.committee_type
        ).first()

        if not requirement:
            return "No Requirement"

        minimum = requirement.minimum_members

        if minimum == 0:
            return "Not Required"

        count = self.committee_member_count(obj)

        if count >= minimum:
            return "✓ Minimum Reached"

        return f"⚠ Need {minimum - count} More"

    committee_status.short_description = "Committee Status"

    def member_id_display(self, obj):
        return obj.member.member_id

    member_id_display.short_description = "Member ID"
    member_id_display.admin_order_field = "member__member_id"

    def member_name(self, obj):
        return obj.member.application.full_name

    member_name.short_description = "Member Name"
    member_name.admin_order_field = "member__application__full_name"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "member":
            kwargs["queryset"] = (
                Member.objects
                .filter(status="active")
                .select_related("application")
                .order_by("member_id")
            )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )

    def save_model(self, request, obj, form, change):
        if obj.member.status != "active":
            raise ValidationError(
                "শুধুমাত্র Active সদস্যকে কমিটিতে যুক্ত করা যাবে।"
            )

        super().save_model(request, obj, form, change)


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]

    search_fields = [
        "name",
    ]

    ordering = [
        "name",
    ]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "division",
    ]

    list_filter = [
        "division",
    ]

    search_fields = [
        "name",
        "division__name",
    ]

    ordering = [
        "division__name",
        "name",
    ]


@admin.register(Upazila)
class UpazilaAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "district",
    ]

    list_filter = [
        "district__division",
        "district",
    ]

    search_fields = [
        "name",
        "district__name",
        "district__division__name",
    ]

    ordering = [
        "district__division__name",
        "district__name",
        "name",
    ]


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "upazila",
    ]

    list_filter = [
        "upazila__district__division",
        "upazila__district",
        "upazila",
    ]

    search_fields = [
        "name",
        "upazila__name",
        "upazila__district__name",
    ]

    ordering = [
        "upazila__district__division__name",
        "upazila__district__name",
        "upazila__name",
        "name",
    ]


@admin.register(UnionWard)
class UnionWardAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "upazila",
    ]

    list_filter = [
        "upazila__district__division",
        "upazila__district",
        "upazila",
    ]

    search_fields = [
        "name",
        "upazila__name",
        "upazila__district__name",
    ]

    ordering = [
        "upazila__district__division__name",
        "upazila__district__name",
        "upazila__name",
        "name",
    ]