from django.urls import path

from . import views


app_name = "team"


urlpatterns = [
    path(
        "",
        views.team_list,
        name="list",
    ),

    path(
        "<slug:slug>/",
        views.team_detail,
        name="detail",
    ),

    # Committee location AJAX endpoints
    path(
        "ajax/districts/",
        views.ajax_districts,
        name="ajax_districts",
    ),

    path(
        "ajax/upazilas/",
        views.ajax_upazilas,
        name="ajax_upazilas",
    ),

    path(
        "ajax/municipalities/",
        views.ajax_municipalities,
        name="ajax_municipalities",
    ),

    path(
        "ajax/union-wards/",
        views.ajax_union_wards,
        name="ajax_union_wards",
    ),
]