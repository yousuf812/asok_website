from django.shortcuts import get_object_or_404, render

from .models import TeamMember


def team_list(request):
    members = TeamMember.objects.filter(
        is_active=True
    ).order_by("order", "name")

    context = {
        "members": members,
    }

    return render(request, "team/list.html", context)


def team_detail(request, slug):
    member = get_object_or_404(
        TeamMember,
        slug=slug,
        is_active=True,
    )

    context = {
        "member": member,
    }

    return render(request, "team/detail.html", context)