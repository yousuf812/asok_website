from django.db import models
from django.utils.text import slugify


class Service(models.Model):

    ICON_CHOICES = [
        ("scale", "Justice Scale"),
        ("shield", "Shield"),
        ("book", "Book"),
        ("users", "Users"),
        ("search", "Search"),
        ("heart", "Heart"),
    ]

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    description = models.TextField()

    icon = models.CharField(
        max_length=20,
        choices=ICON_CHOICES,
        default="scale"
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

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
        ordering = ["order", "-created_at"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title