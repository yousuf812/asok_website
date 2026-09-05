import uuid

from django.db import models


class Complaint(models.Model):

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("investigating", "Investigating"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    CATEGORY_CHOICES = [
        ("violence", "Violence or Abuse"),
        ("discrimination", "Discrimination"),
        ("harassment", "Harassment"),
        ("land", "Land or Property"),
        ("employment", "Employment"),
        ("family", "Family Matter"),
        ("other", "Other"),
    ]

    CONTACT_CHOICES = [
        ("phone", "Phone"),
        ("email", "Email"),
    ]

    complaint_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    complainant_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Leave blank if you want to remain anonymous."
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    subject = models.CharField(
        max_length=200
    )

    incident_date = models.DateField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=250,
        blank=True
    )

    description = models.TextField()

    preferred_contact = models.CharField(
        max_length=20,
        choices=CONTACT_CHOICES,
        blank=True
    )

    is_anonymous = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="submitted"
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
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"

    def save(self, *args, **kwargs):

        if not self.complaint_id:
            self.complaint_id = (
                f"ASOK-C-{uuid.uuid4().hex[:8].upper()}"
            )

        if self.is_anonymous:
            self.complainant_name = ""
            self.email = ""
            self.phone = ""
            self.preferred_contact = ""

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.complaint_id} - {self.subject}"