from django.urls import path

from . import views


app_name = "legal_aid"


urlpatterns = [

    path(
        "",
        views.legal_aid_home,
        name="home"
    ),

    path(
        "success/",
        views.legal_aid_success,
        name="success"
    ),

]