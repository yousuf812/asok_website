from django.shortcuts import render

from .models import OrganizationInfo
from services.models import Service
from team.models import TeamMember
from activities.models import Activity, ImpactStatistic
from blog.models import BlogPost
from gallery.models import GalleryImage
from django.http import HttpResponse
from projects.models import Project


def home(request):

    organization = OrganizationInfo.objects.first()

    services = Service.objects.filter(
        is_active=True
    ).order_by(
        "order",
        "-created_at"
    )

    team_members = TeamMember.objects.filter(
        is_active=True
    ).order_by(
        "order",
        "name"
    )

    featured_team = team_members.filter(
        is_featured=True
    )

    featured_activities = Activity.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by(
        "order",
        "-start_date",
        "-created_at"
    )[:6]

    impact_stats = ImpactStatistic.objects.filter(
        is_active=True
    ).order_by(
        "order",
        "id"
    )[:4]

    latest_posts = BlogPost.objects.filter(
        status="published"
    ).select_related(
        "category"
    ).order_by(
        "-published_at",
        "-created_at"
    )[:3]


    latest_projects = Project.objects.filter(
    is_active=True
).order_by(
    "-published_date",
    "-created_at",
)[:3]

    featured_gallery = GalleryImage.objects.filter(
    is_active=True,
    is_featured=True,
).select_related(
    "category"
).order_by(
    "order",
    "-taken_at",
    "-created_at"
)[:6]

    context = {
        "organization": organization,
        "services": services,
        "team_members": team_members,
        "featured_team": featured_team,
        "featured_activities": featured_activities,
        "impact_stats": impact_stats,
        "latest_posts": latest_posts,
        "featured_gallery": featured_gallery,
        "latest_projects": latest_projects,
    }

    return render(
        request,
        "core/home.html",
        context
    )


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def terms_conditions(request):
    return render(request, "core/terms_conditions.html")


def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: /sitemap.xml
"""

    return HttpResponse(
        content,
        content_type="text/plain"
    )

