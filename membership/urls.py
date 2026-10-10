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

    path(
    "set-password/<str:member_id>/",
    views.member_set_password,
    name="set_password",
),

path("login/", views.member_login, name="login"),
path("logout/", views.member_logout, name="logout"),
path("dashboard/", views.member_dashboard, name="dashboard"),

path(
    "payment/",
    views.member_monthly_payment,
    name="monthly_payment",
),

path(
    "payment/success/",
    views.member_payment_success,
    name="payment_success",
),

path(
    "change-password/",
    views.member_change_password,
    name="change_password",
),

path(
    "profile/edit/",
    views.member_profile_edit,
    name="profile_edit",
),

path(
    "profile/photo/",
    views.member_photo_update,
    name="photo_update",
),

path(
    "password-reset/",
    views.member_password_reset,
    name="password_reset",
),

path(
    "password-reset/done/",
    views.member_password_reset_done,
    name="password_reset_done",
),

path(
    "password-reset/confirm/<uidb64>/<token>/",
    views.member_password_reset_confirm,
    name="password_reset_confirm",
),
]