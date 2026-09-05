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
]