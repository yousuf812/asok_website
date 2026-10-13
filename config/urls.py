from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.urls import re_path
from django.views.static import serve


from core.sitemaps import (
    StaticViewSitemap,
    BlogPostSitemap,
    ActivitySitemap,
    GalleryImageSitemap,
    HumanRightsArticleSitemap,
)




urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("core.urls")),

    path( "human-rights/", include("human_rights.urls")),
    
    path( "legal-aid/",include("legal_aid.urls")),

    path( "complaint/",include("complaints.urls")),
    path( "activities/",include("activities.urls")),
    path("blog/", include("blog.urls")),
    path("gallery/",include("gallery.urls")),
    path("join-us/", include("membership.urls")),
     path("donate/", include("donations.urls")),
      path("contact/", include("contacts.urls")),
      path("newsletter/",include("newsletter.urls")),
      path( "projects/", include("projects.urls")),
      path("team/", include("team.urls")),
      re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),

      path(
    "sitemap.xml",
    sitemap,
    {
        "sitemaps": {
            "static": StaticViewSitemap,
            "blog": BlogPostSitemap,
            "activities": ActivitySitemap,
            "gallery": GalleryImageSitemap,
            "human_rights": HumanRightsArticleSitemap,
        }
    },
    name="sitemap",
),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )