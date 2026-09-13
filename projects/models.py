from django.db import models
from django.urls import reverse


class Project(models.Model):

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
    )

    description = models.TextField()

    published_date = models.DateField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Show this project on the website.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-published_date", "-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def save(self, *args, **kwargs):

        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "projects:detail",
            kwargs={"slug": self.slug},
        )

    def __str__(self):
        return self.title