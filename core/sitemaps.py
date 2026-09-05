from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from activities.models import Activity
from blog.models import BlogPost
from gallery.models import GalleryImage
from human_rights.models import HumanRightsArticle


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "core:privacy_policy",
            "core:terms_conditions",
            "human_rights:home",
            "legal_aid:home",
            "activities:list",
            "blog:list",
            "gallery:list",
            "membership:home",
            "donations:home",
            "contacts:home",
            "newsletter:subscribe",
        ]

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return BlogPost.objects.filter(
            status="published"
        ).order_by("-published_at")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse(
            "blog:detail",
            kwargs={"slug": obj.slug},
        )


class ActivitySitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Activity.objects.all().order_by("-created_at")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse(
            "activities:detail",
            kwargs={"slug": obj.slug},
        )


class GalleryImageSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return GalleryImage.objects.filter(
            is_active=True
        ).order_by("-created_at")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse(
            "gallery:detail",
            kwargs={"slug": obj.slug},
        )


class HumanRightsArticleSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return HumanRightsArticle.objects.filter(
            is_published=True
        ).order_by("-created_at")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse(
            "human_rights:article_detail",
            kwargs={"slug": obj.slug},
        )