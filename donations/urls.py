from django.urls import path

from . import views


app_name = "donations"


urlpatterns = [

    path(
        "",
        views.donation_home,
        name="home",
    ),

    path(
        "success/",
        views.donation_success,
        name="success",
    ),

    path(
        "dashboard/",
        views.donation_dashboard,
        name="dashboard",
    ),

    path(
        "lookup/",
        views.donation_lookup,
        name="lookup",
    ),
]