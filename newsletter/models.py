from django.db import models


class Subscriber(models.Model):

    email = models.EmailField(
        unique=True
    )

    is_active = models.BooleanField(
        default=True
    )

    subscribed_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-subscribed_at"]
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email