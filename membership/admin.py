from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User

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
        "member_id",
        "member_name",
        "payment_type",
        "amount",
        "payment_month",
        "payment_method",
        "status",
        "transaction_id",
        "paid_at",
        "created_at",
    ]

    list_filter = [
        "payment_type",
        "status",
        "payment_method",
        "payment_month",
        "created_at",
    ]

    search_fields = [
        "application__member__member_id",
        "application__full_name",
        "application__email",
        "transaction_id",
    ]

    readonly_fields = [
        "paid_at",
        "created_at",
        "updated_at",
    ]

    autocomplete_fields = [
        "application",
    ]

    date_hierarchy = "created_at"

    ordering = [
        "-created_at",
    ]

    fieldsets = (
        (
            "Payment Information",
            {
                "fields": (
                    "application",
                    "payment_type",
                    "amount",
                    "payment_month",
                )
            },
        ),
        (
            "Payment Details",
            {
                "fields": (
                    "payment_method",
                    "transaction_id",
                    "status",
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

    @admin.display(
        description="Member ID",
        ordering="application__member__member_id",
    )
    def member_id(self, obj):
        if hasattr(obj.application, "member"):
            return obj.application.member.member_id

        return "-"

    @admin.display(
        description="Member Name",
        ordering="application__full_name",
    )
    def member_name(self, obj):
        return obj.application.full_name

    def save_model(self, request, obj, form, change):

        if obj.status == "paid":
            if not obj.paid_at:
                obj.paid_at = timezone.now()

        else:
            obj.paid_at = None

        super().save_model(request, obj, form, change)

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
        "member_name",
        "status",
        "effective_status_display",
        "activation_date",
        "user",
        "joined_at",
    ]

    list_filter = [
        "status",
        "activation_date",
        "joined_at",
    ]

    search_fields = [
        "member_id",
        "application__full_name",
        "application__email",
        "application__phone",
    ]

    readonly_fields = [
        "member_id",
        "joined_at",
        "updated_at",
        "activation_token",
        "activation_token_created_at",
    ]

    autocomplete_fields = [
        "application",
        "user",
    ]

    actions = [
        "create_member_accounts",
    ]

    fieldsets = (
        (
            "Member Information",
            {
                "fields": (
                    "application",
                    "member_id",
                    "status",
                    "activation_date",
                )
            },
        ),
        (
            "Login Account",
            {
                "fields": (
                    "user",
                    "activation_token",
                    "activation_token_created_at",
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
    def member_name(self, obj):
        return obj.application.full_name

    @admin.display(
        description="Effective Status",
    )
    def effective_status_display(self, obj):
        return obj.effective_status_display

    @admin.action(
        description="Create login account for selected members"
    )
    def create_member_accounts(self, request, queryset):

        created_count = 0
        skipped_count = 0

        for member in queryset.select_related("application", "user"):

            # Already has an account
            if member.user:
                skipped_count += 1
                continue

            # Only active members can receive accounts
            if member.status != "active":
                skipped_count += 1
                continue

            application = member.application

            username = member.member_id.lower()

            # Existing username protection
            if User.objects.filter(username=username).exists():
                skipped_count += 1
                continue

            # Create user account
            user = User.objects.create_user(
                username=username,
                email=application.email,
                first_name=application.full_name,
                is_active=True,
            )

            # User cannot login until password is created
            user.set_unusable_password()
            user.save()

            # Create secure activation token
            member.activation_token = uuid.uuid4()
            member.activation_token_created_at = timezone.now()

            member.user = user

            member.save(
                update_fields=[
                    "user",
                    "activation_token",
                    "activation_token_created_at",
                    "updated_at",
                ]
            )

            created_count += 1

            activation_url = request.build_absolute_uri(
                f"/join-us/set-password/{member.member_id}/"
                f"?token={member.activation_token}"
            )

            self.message_user(
                request,
                (
                    f"Account created for {member.member_id}. "
                    f"Activation URL: {activation_url}"
                ),
                messages.SUCCESS,
            )

        if created_count == 0:
            self.message_user(
                request,
                "No new member account was created.",
                messages.WARNING,
            )

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

    