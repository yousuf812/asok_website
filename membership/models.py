import uuid

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