from django.shortcuts import render

from .models import Project
from django.shortcuts import get_object_or_404, render




def project_list(request):
    projects = Project.objects.filter(
        is_active=True
    ).order_by(
        "-published_date",
        "-created_at",
    )

    context = {
        "projects": projects,
    }

    return render(
        request,
        "projects/list.html",
        context,
    )


def project_detail(request, slug):
    project = get_object_or_404(
        Project,
        slug=slug,
        is_active=True,
    )

    context = {
        "project": project,
    }

    return render(
        request,
        "projects/detail.html",
        context,
    )