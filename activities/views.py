from django.shortcuts import get_object_or_404, render

from .models import Activity
from django.urls import reverse


def activity_list(request):
    activities = Activity.objects.filter(
        is_active=True
    ).order_by(
        "order",
        "-start_date",
        "-created_at",
    )

    context = {
    "activity": activity,
    "breadcrumb_items": [
        {
            "name": "Activities",
            "url": reverse("activities:list"),
        },
        {
            "name": activity.title,
            "url": reverse(
                "activities:detail",
                kwargs={"slug": activity.slug},
            ),
        },
    ],
}

    return render(
        request,
        "activities/list.html",
        context,
    )


def activity_detail(request, slug):
    activity = get_object_or_404(
        Activity,
        slug=slug,
        is_active=True,
    )

    context = {
        "activity": activity,
    }

    return render(
        request,
        "activities/detail.html",
        context,
    )