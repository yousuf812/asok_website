from django.urls import path

from . import views


app_name = "membership"


urlpatterns = [
    path(
        "",
        views.membership_home,
        name="home",
    ),

    path(
        "success/",
        views.membership_success,
        name="success",
    ),

    path(
        "verify/",
        views.member_search,
        name="member_search",
    ),

    path(
        "verify/<str:member_id>/",
        views.member_verify,
        name="verify",
    ),

    path(
        "card/<str:member_id>/",
        views.member_card,
        name="card",
    ),
]