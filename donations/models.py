import uuid

from django.db import models


class Donation(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("bank", "Bank Transfer"),
        ("bkash", "bKash"),
        ("nagad", "Nagad"),
        ("cash", "Cash"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    PURPOSE_CHOICES = [
        ("general", "General Support"),
        ("human_rights", "Human Rights"),
        ("legal_aid", "Legal Aid"),
        ("community", "Community Development"),
        ("awareness", "Awareness Programs"),
        ("other", "Other"),
    ]

    reference_number = models.CharField(
        max_length=25,
        unique=True,
        editable=False,
    )

    donor_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Leave blank if the donor wants to remain anonymous.",
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    purpose = models.CharField(
        max_length=30,
        choices=PURPOSE_CHOICES,
        default="general",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True,
        help_text="Payment transaction ID, if available.",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    message = models.TextField(
        blank=True,
        help_text="Optional message from the donor.",
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
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

    def save(self, *args, **kwargs):

        if not self.reference_number:
            self.reference_number = (
                f"ASOK-D-{uuid.uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} - {self.amount}"