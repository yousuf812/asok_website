from django.db import models
from django.utils.text import slugify


class TeamMember(models.Model):

    ROLE_CHOICES = [
        ("founder", "Founder"),
        ("director", "Director"),
        ("coordinator", "Coordinator"),
        ("legal_advisor", "Legal Advisor"),
        ("human_rights", "Human Rights Officer"),
        ("member", "Team Member"),
    ]

    name = models.CharField(max_length=150)

    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
    )

    designation = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default="member",
    )

    bio = models.TextField(
        blank=True,
        help_text="Short biography of the team member.",
    )

    photo = models.ImageField(
        upload_to="team/",
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    facebook_url = models.URLField(
        blank=True,
    )

    linkedin_url = models.URLField(
        blank=True,
    )

    website_url = models.URLField(
        blank=True,
    )

    is_featured = models.BooleanField(
        default=False,
        help_text="Show this member in the featured team section.",
    )

    is_active = models.BooleanField(
        default=True,
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Lower number appears first.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_designation_display()}"