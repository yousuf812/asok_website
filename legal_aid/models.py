import uuid

from django.db import models


class LegalAidRequest(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("rejected", "Rejected"),
    ]

    CONTACT_CHOICES = [
        ("phone", "Phone"),
        ("email", "Email"),
    ]

    CATEGORY_CHOICES = [
        ("land", "Land & Property"),
        ("family", "Family Matter"),
        ("violence", "Violence & Abuse"),
        ("employment", "Employment"),
        ("discrimination", "Discrimination"),
        ("other", "Other"),
    ]

    reference_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    full_name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    subject = models.CharField(
        max_length=200
    )

    description = models.TextField()

    preferred_contact = models.CharField(
        max_length=20,
        choices=CONTACT_CHOICES,
        default="phone"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    admin_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Legal Aid Request"
        verbose_name_plural = "Legal Aid Requests"

    def save(self, *args, **kwargs):

        if not self.reference_number:
            self.reference_number = (
                f"ASOK-{uuid.uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} - {self.full_name}"