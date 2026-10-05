from django.urls import path

from . import views


app_name = "team"


urlpatterns = [
    path("", views.team_list, name="list"),
    path("committee/", views.committee_list, name="committee_list"),
    path("committee/member/<int:pk>/", views.committee_member_detail,name="committee_member_detail"),
    path( "committee/search/",views.committee_search,name="committee_search"),
    path("ajax/districts/", views.ajax_districts, name="ajax_districts"),
    path("ajax/upazilas/", views.ajax_upazilas, name="ajax_upazilas"),
    path("ajax/municipalities/", views.ajax_municipalities, name="ajax_municipalities"),
    path("ajax/union-wards/", views.ajax_union_wards, name="ajax_union_wards"),
    path("<slug:slug>/", views.team_detail, name="detail"),   # ← সবার শেষে
]