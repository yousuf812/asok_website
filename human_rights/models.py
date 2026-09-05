from django.db import models
from django.utils.text import slugify


class HumanRightsCategory(models.Model):

    name = models.CharField(
        max_length=150
    )

    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
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
        ordering = ["order", "name"]
        verbose_name = "Human Rights Category"
        verbose_name_plural = "Human Rights Categories"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class HumanRightsArticle(models.Model):

    category = models.ForeignKey(
        HumanRightsCategory,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    title = models.CharField(
        max_length=250
    )

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True
    )

    short_description = models.TextField(
        max_length=500
    )

    content = models.TextField()

    image = models.ImageField(
        upload_to="human_rights/",
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(
        default=False
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
        ordering = ["order", "-created_at"]
        verbose_name = "Human Rights Article"
        verbose_name_plural = "Human Rights Articles"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class HumanRightsFAQ(models.Model):

    question = models.CharField(
        max_length=300
    )

    answer = models.TextField()

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
        ordering = ["order", "-created_at"]
        verbose_name = "Human Rights FAQ"
        verbose_name_plural = "Human Rights FAQs"

    def __str__(self):
        return self.question