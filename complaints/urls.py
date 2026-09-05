from django.urls import path

from . import views


app_name = "complaints"


urlpatterns = [

    path(
        "",
        views.complaint_home,
        name="home"
    ),

    path(
        "success/",
        views.complaint_success,
        name="success"
    ),

]