from django.shortcuts import get_object_or_404, render

from .models import TeamMember
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import (
    Division,
    District,
    Upazila,
    Municipality,
    UnionWard,
)


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


def ajax_districts(request):
    division_id = request.GET.get("division_id")

    if not division_id:
        return JsonResponse(
            {
                "results": [],
            }
        )

    districts = District.objects.filter(
        division_id=division_id
    ).order_by("name")

    results = [
        {
            "id": district.id,
            "name": district.name,
        }
        for district in districts
    ]

    return JsonResponse(
        {
            "results": results,
        }
    )


def ajax_upazilas(request):
    district_id = request.GET.get("district_id")

    if not district_id:
        return JsonResponse(
            {
                "results": [],
            }
        )

    upazilas = Upazila.objects.filter(
        district_id=district_id
    ).order_by("name")

    results = [
        {
            "id": upazila.id,
            "name": upazila.name,
        }
        for upazila in upazilas
    ]

    return JsonResponse(
        {
            "results": results,
        }
    )


def ajax_municipalities(request):
    upazila_id = request.GET.get("upazila_id")

    if not upazila_id:
        return JsonResponse(
            {
                "results": [],
            }
        )

    municipalities = Municipality.objects.filter(
        upazila_id=upazila_id
    ).order_by("name")

    results = [
        {
            "id": municipality.id,
            "name": municipality.name,
        }
        for municipality in municipalities
    ]

    return JsonResponse(
        {
            "results": results,
        }
    )


def ajax_union_wards(request):
    upazila_id = request.GET.get("upazila_id")

    if not upazila_id:
        return JsonResponse(
            {
                "results": [],
            }
        )

    union_wards = UnionWard.objects.filter(
        upazila_id=upazila_id
    ).order_by("name")

    results = [
        {
            "id": union_ward.id,
            "name": union_ward.name,
        }
        for union_ward in union_wards
    ]

    return JsonResponse(
        {
            "results": results,
        }
    )