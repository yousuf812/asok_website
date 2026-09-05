from django.urls import path

from . import views


app_name = "contacts"


urlpatterns = [

    path(
        "",
        views.contact_home,
        name="home",
    ),

    path(
        "success/",
        views.contact_success,
        name="success",
    ),
]