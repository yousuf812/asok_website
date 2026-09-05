from django.db import models
from django.utils.text import slugify


class Activity(models.Model):

    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("upcoming", "Upcoming"),
    ]

    CATEGORY_CHOICES = [
        ("human_rights", "Human Rights"),
        ("legal_aid", "Legal Aid"),
        ("awareness", "Awareness"),
        ("community", "Community Development"),
        ("training", "Training & Workshop"),
        ("research", "Research"),
        ("other", "Other"),
    ]

    title = models.CharField(
        max_length=250
    )

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="human_rights"
    )

    short_description = models.TextField(
        max_length=500,
        help_text="Short description shown on activity cards."
    )

    description = models.TextField(
        help_text="Full activity/project description."
    )

    image = models.ImageField(
        upload_to="activities/",
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=250,
        blank=True
    )

    start_date = models.DateField(
        blank=True,
        null=True
    )

    end_date = models.DateField(
        blank=True,
        null=True
    )

    beneficiaries = models.PositiveIntegerField(
        default=0,
        help_text="Approximate number of people benefited."
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="upcoming"
    )

    is_featured = models.BooleanField(
        default=False,
        help_text="Show this activity on the homepage."
    )

    is_active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Lower number appears first."
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["order", "-start_date", "-created_at"]
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ImpactStatistic(models.Model):

    title = models.CharField(
        max_length=100,
        help_text="Example: People Reached"
    )

    value = models.PositiveIntegerField(
        default=0,
        help_text="Example: 500"
    )

    suffix = models.CharField(
        max_length=10,
        default="+",
        blank=True,
        help_text="Example: +, %, K"
    )

    description = models.CharField(
        max_length=200,
        blank=True
    )

    icon = models.CharField(
        max_length=30,
        default="users",
        help_text="Icon identifier for frontend."
    )

    is_active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "order",
            "id",
        ]

        verbose_name = "Impact Statistic"
        verbose_name_plural = "Impact Statistics"

    def __str__(self):
        return f"{self.title} - {self.value}{self.suffix}"