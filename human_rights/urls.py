from django.urls import path

from . import views


app_name = "human_rights"


urlpatterns = [

    path(
        "",
        views.human_rights_home,
        name="home"
    ),

    path(
        "article/<slug:slug>/",
        views.human_rights_article,
        name="article"
    ),

]