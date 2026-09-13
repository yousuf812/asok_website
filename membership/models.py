import uuid

from django.core.exceptions import ValidationError
from django.db import models


class MembershipApplication(models.Model):

    MEMBERSHIP_TYPES = [
        ("volunteer", "Volunteer"),
        ("member", "General Member"),
        ("student", "Student Volunteer"),
        ("professional", "Professional Member"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    INTEREST_CHOICES = [
        ("human_rights", "Human Rights"),
        ("legal_aid", "Legal Aid"),
        ("awareness", "Awareness Campaign"),
        ("community", "Community Development"),
        ("research", "Research"),
        ("training", "Training & Workshop"),
        ("other", "Other"),
    ]

    reference_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    full_name = models.CharField(
        max_length=150,
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
    )

    membership_type = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_TYPES,
        default="volunteer",
    )

    profession = models.CharField(
        max_length=150,
        blank=True,
    )

    address = models.CharField(
        max_length=300,
    )

    # =====================================================
    # IDENTITY INFORMATION
    # =====================================================

    nid_number = models.CharField(
        max_length=30,
        blank=True,
        help_text="National ID (NID) number.",
    )

    birth_registration_number = models.CharField(
        max_length=30,
        blank=True,
        help_text="Birth Registration number.",
    )

    photo = models.ImageField(
        upload_to="membership/photos/",
        blank=True,
        null=True,
        help_text="Member's recent passport-size photo.",
    )

    # =====================================================
    # MEMBERSHIP INFORMATION
    # =====================================================

    area_of_interest = models.CharField(
        max_length=30,
        choices=INTEREST_CHOICES,
    )

    motivation = models.TextField(
        help_text="Why do you want to join ASOK Foundation?",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    admin_notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Membership Application"
        verbose_name_plural = "Membership Applications"

    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = (
                f"ASOK-M-{uuid.uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} - {self.full_name}"


class MembershipPayment(models.Model):

    PAYMENT_TYPE_CHOICES = [
        ("registration", "Registration Fee"),
        ("monthly", "Monthly Fee"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("bkash", "bKash"),
        ("nagad", "Nagad"),
        ("bank", "Bank Transfer"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    application = models.ForeignKey(
        MembershipApplication,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="cash",
    )

    payment_month = models.DateField(
        blank=True,
        null=True,
        help_text="For monthly fee, select the month this payment covers.",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="bKash/Nagad/Bank transaction ID if applicable.",
    )

    notes = models.TextField(
        blank=True,
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Membership Payment"
        verbose_name_plural = "Membership Payments"

    def __str__(self):
        return (
            f"{self.application.full_name} - "
            f"{self.get_payment_type_display()} - "
            f"{self.amount}"
        )


class MembershipFeeSettings(models.Model):

    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000,
        help_text="One-time registration fee.",
    )

    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=100,
        help_text="Monthly membership fee.",
    )

    is_active = models.BooleanField(
        default=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Membership Fee Settings"
        verbose_name_plural = "Membership Fee Settings"

    def __str__(self):
        return "Membership Fee Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class Member(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("suspended", "Suspended"),
    ]

    application = models.OneToOneField(
        MembershipApplication,
        on_delete=models.CASCADE,
        related_name="member",
    )

    member_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    activation_date = models.DateField(
        blank=True,
        null=True,
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-joined_at"]
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def save(self, *args, **kwargs):
        if not self.member_id:
            last_member = (
                Member.objects
                .order_by("-id")
                .first()
            )

            if last_member and last_member.member_id:
                try:
                    last_number = int(
                        last_member.member_id.split("-")[1]
                    )
                except (ValueError, IndexError):
                    last_number = 0
            else:
                last_number = 0

            self.member_id = f"ASOK-{last_number + 1:09d}"

        super().save(*args, **kwargs)

    def clean(self):
        if self.status != "active":
            return

        if self.application.status != "approved":
            raise ValidationError(
                "A member can only be activated after "
                "the application is approved."
            )

        registration_paid = self.application.payments.filter(
            payment_type="registration",
            status="paid",
        ).exists()

        if not registration_paid:
            raise ValidationError(
                "Registration fee must be paid before "
                "activating this member."
            )

    def __str__(self):
        return f"{self.member_id} - {self.application.full_name}"


class MemberPromotion(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="promotions",
    )

    designation = models.CharField(
        max_length=150,
        help_text="New position or designation.",
    )

    effective_date = models.DateField()

    notes = models.TextField(
        blank=True,
        help_text="Optional notes about this promotion.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-effective_date", "-created_at"]
        verbose_name = "Member Promotion"
        verbose_name_plural = "Member Promotions"

    def __str__(self):
        return (
            f"{self.member.member_id} - "
            f"{self.designation}"
        )