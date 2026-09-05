from django.db import models


class OrganizationInfo(models.Model):
    title = models.CharField(max_length=200, default="About ASOK")

    short_description = models.TextField(
        help_text="Short description for the homepage."
    )

    full_description = models.TextField(
        help_text="Main organization description."
    )

    mission = models.TextField(
        help_text="Organization mission."
    )

    vision = models.TextField(
        help_text="Organization vision."
    )

    image = models.ImageField(
        upload_to="organization/",
        blank=True,
        null=True
    )

    email = models.EmailField(
        default="info@asok.info",
        help_text="Official organization email."
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        help_text="Official phone number."
    )

    address = models.CharField(
        max_length=300,
        blank=True,
        help_text="Office address."
    )

    facebook_url = models.URLField(
        blank=True,
        help_text="Official Facebook page URL."
    )

    linkedin_url = models.URLField(
        blank=True,
        help_text="Official LinkedIn page URL."
    )

    youtube_url = models.URLField(
        blank=True,
        help_text="Official YouTube channel URL."
    )

    updated_at = models.DateTimeField(auto_now=True)