from django.contrib import admin
from .models import (
    MembershipApplication,
    MembershipPayment,
    MembershipFeeSettings,
    Member, MemberPromotion,
)


@admin.action(description="Create members from approved applications")
def create_members_from_applications(modeladmin, request, queryset):
    created_count = 0
    skipped_count = 0

    for application in queryset:
        if application.status != "approved":
            skipped_count += 1
            continue

        if hasattr(application, "member"):
            skipped_count += 1
            continue

        Member.objects.create(
            application=application,
        )

        created_count += 1

    if created_count:
        modeladmin.message_user(
            request,
            f"{created_count} member(s) created successfully.",
        )

    if skipped_count:
        modeladmin.message_user(
            request,
            f"{skipped_count} application(s) skipped.",
        )


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):

    actions = [
    "create_members_from_applications",
]

    list_display = [
        "reference_number",
        "full_name",
        "email",
        "phone",
        "membership_type",
        "nid_number",
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
        "nid_number",
        "birth_registration_number",
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
            "Identity Information",
            {
                "fields": (
                    "nid_number",
                    "birth_registration_number",
                    "photo",
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



@admin.register(MembershipPayment)
class MembershipPaymentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "application",
        "payment_type",
        "amount",
        "payment_method",
        "payment_month",
        "status",
        "paid_at",
        "created_at",
    ]

    list_filter = [
        "payment_type",
        "payment_method",
        "status",
        "payment_month",
        "created_at",
    ]

    search_fields = [
        "application__reference_number",
        "application__full_name",
        "application__email",
        "application__phone",
        "transaction_id",
    ]

    list_editable = [
        "status",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    date_hierarchy = "created_at"

    ordering = [
        "-created_at",
    ]

    fieldsets = (
        (
            "Member / Application",
            {
                "fields": (
                    "application",
                )
            },
        ),
        (
            "Payment Information",
            {
                "fields": (
                    "payment_type",
                    "amount",
                    "payment_method",
                    "payment_month",
                    "status",
                    "transaction_id",
                    "paid_at",
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
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(MembershipFeeSettings)
class MembershipFeeSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "registration_fee",
        "monthly_fee",
        "is_active",
        "updated_at",
    ]

    fields = [
        "registration_fee",
        "monthly_fee",
        "is_active",
        "updated_at",
    ]

    readonly_fields = [
        "updated_at",
    ]

    def has_add_permission(self, request):
        # Only one fee-settings record is allowed.
        if MembershipFeeSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False



def save_model(self, request, obj, form, change):
    if obj.payment_type == "monthly" and not obj.payment_month:
        raise ValueError(
            "Payment month is required for monthly membership fees."
        )

    if obj.status == "paid" and not obj.paid_at:
        from django.utils import timezone
        obj.paid_at = timezone.now()

    super().save_model(request, obj, form, change)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = [
        "member_id",
        "get_full_name",
        "get_membership_type",
        "status",
        "activation_date",
        "joined_at",
    ]

    list_filter = [
        "status",
        "application__membership_type",
        "activation_date",
        "joined_at",
    ]

    search_fields = [
        "member_id",
        "application__full_name",
        "application__email",
        "application__phone",
        "application__reference_number",
        "application__nid_number",
        "application__birth_registration_number",
    ]

    list_editable = [
        "status",
    ]

    readonly_fields = [
        "member_id",
        "joined_at",
        "updated_at",
    ]

    ordering = [
        "-joined_at",
    ]

    date_hierarchy = "joined_at"

    fieldsets = (
        (
            "Member Information",
            {
                "fields": (
                    "member_id",
                    "application",
                    "status",
                    "activation_date",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "joined_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(
        description="Member Name",
        ordering="application__full_name",
    )
    def get_full_name(self, obj):
        return obj.application.full_name

    @admin.display(
        description="Membership Type",
        ordering="application__membership_type",
    )
    def get_membership_type(self, obj):
        return obj.application.get_membership_type_display()

def save_model(self, request, obj, form, change):
    from django.utils import timezone

    if obj.status == "active" and not obj.activation_date:
        obj.activation_date = timezone.localdate()

    if obj.status != "active":
        obj.activation_date = None

    super().save_model(request, obj, form, change)


@admin.register(MemberPromotion)
class MemberPromotionAdmin(admin.ModelAdmin):

    list_display = [
        "get_member_id",
        "get_full_name",
        "designation",
        "effective_date",
        "created_at",
    ]

    list_filter = [
        "designation",
        "effective_date",
        "created_at",
    ]

    search_fields = [
        "member__member_id",
        "member__application__full_name",
        "member__application__email",
        "member__application__phone",
        "designation",
        "notes",
    ]

    readonly_fields = [
        "created_at",
    ]

    date_hierarchy = "effective_date"

    ordering = [
        "-effective_date",
        "-created_at",
    ]

    fieldsets = (
        (
            "Promotion Information",
            {
                "fields": (
                    "member",
                    "designation",
                    "effective_date",
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
            "System Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    @admin.display(
        description="Member ID",
        ordering="member__member_id",
    )
    def get_member_id(self, obj):
        return obj.member.member_id

    @admin.display(
        description="Member Name",
        ordering="member__application__full_name",
    )
    def get_full_name(self, obj):
        return obj.member.application.full_name

    