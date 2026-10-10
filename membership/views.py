from django.contrib import messages
from .forms import MembershipApplicationForm
from core.email_utils import send_admin_notification
import base64
from io import BytesIO
import qrcode
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import MemberMonthlyPaymentForm
from .models import Member, MembershipFeeSettings, MembershipPayment
from datetime import timedelta
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode






def membership_home(request):

    if request.method == "POST":

        form = MembershipApplicationForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            application = form.save()
            fee_settings = MembershipFeeSettings.objects.filter(
             is_active=True
            ).first()

            if fee_settings:
                MembershipPayment.objects.create(
                application=application,
                 payment_type="registration",
                amount=fee_settings.registration_fee,
                payment_method="cash",
                status="pending",
            )

            send_admin_notification(
                subject=(
                    f"New Membership Application — "
                    f"{application.full_name}"
                ),
                message=(
                    f"Name: {application.full_name}\n"
                    f"Father's Name: {application.father_name}\n"
                    f"Mother's Name: {application.mother_name}\n"
                    f"Email: {application.email}\n"
                    f"Phone: {application.phone}\n"
                    f"Membership Type: "
                    f"{application.get_membership_type_display()}\n"
                    f"NID: "
                    f"{application.nid_number or 'Not provided'}\n"
                    f"Birth Registration: "
                    f"{application.birth_registration_number or 'Not provided'}\n\n"
                    f"Membership Type: "
                    f"{application.get_membership_type_display()}\n"
                    f"Message:\n"
                    f"{application.motivation}"
                ),
            )

            request.session["membership_reference"] = (
                application.reference_number
            )

            messages.success(
                request,
                "Your membership application has been submitted successfully.",
            )

            return redirect("membership:success")

    else:

        form = MembershipApplicationForm()

    return render(
        request,
        "membership/home.html",
        {
            "form": form,
        },
    )


def membership_success(request):

    reference_number = request.session.get(
        "membership_reference"
    )

    return render(
        request,
        "membership/success.html",
        {
            "reference_number": reference_number,
        },
    )





def member_verify(request, member_id):
    member = get_object_or_404(
        Member.objects.select_related(
            "application"
        ),
        member_id=member_id,
    )

    promotion = (
        member.promotions
        .order_by(
            "-effective_date",
            "-created_at",
        )
        .first()
    )

    # Public verification URL
    verification_url = request.build_absolute_uri(
        reverse(
            "membership:verify",
            kwargs={
                "member_id": member.member_id,
            },
        )
    )

    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(verification_url)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    # Convert QR image to base64
    buffer = BytesIO()

    qr_image.save(
        buffer,
        format="PNG",
    )

    qr_code = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    context = {
        "member": member,
        "promotion": promotion,
        "verification_url": verification_url,
        "qr_code": qr_code,
        "effective_status": member.effective_status,
        "effective_status_display": member.effective_status_display,
    }

    return render(
        request,
        "membership/verify.html",
        context,
    )



def member_card(request, member_id):
    member = get_object_or_404(
        Member.objects.select_related(
            "application"
        ),
        member_id=member_id,
    )

    promotion = (
        member.promotions
        .order_by(
            "-effective_date",
            "-created_at",
        )
        .first()
    )

    # Public verification URL
    verification_url = request.build_absolute_uri(
        reverse(
            "membership:verify",
            kwargs={
                "member_id": member.member_id,
            },
        )
    )

    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(verification_url)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    # Convert QR image to base64
    buffer = BytesIO()

    qr_image.save(
        buffer,
        format="PNG",
    )

    qr_code = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    context = {
        "member": member,
        "promotion": promotion,
        "qr_code": qr_code,
        "verification_url": verification_url,
        "effective_status": member.effective_status,
        "effective_status_display": member.effective_status_display,
    }

    return render(
        request,
        "membership/card.html",
        context,
    )



def member_search(request):
    member_id = request.GET.get("member_id", "").strip()

    if not member_id:
        return render(
            request,
            "membership/member_search.html",
        )

    member = (
        Member.objects
        .select_related("application")
        .filter(member_id__iexact=member_id)
        .first()
    )

    if member:
        return redirect(
            "membership:verify",
            member_id=member.member_id,
        )

    return render(
        request,
        "membership/member_search.html",
        {
            "member_id": member_id,
            "error": "No member found with this Member ID.",
        },
    )


def member_set_password(request, member_id):
    member = get_object_or_404(
        Member.objects.select_related("application", "user"),
        member_id=member_id,
    )

    token = request.GET.get("token", "").strip()

    error = ""

    # Account check
    if not member.user:
        error = "Login account has not been created yet."

    # Token check
    elif not token:
        error = "Invalid or missing activation token."

    elif str(member.activation_token) != token:
        error = "This activation link is invalid."

    # Token expiry check
    elif not member.activation_token_created_at:
        error = "This activation link is no longer valid."

    elif timezone.now() > (
        member.activation_token_created_at + timedelta(hours=24)
    ):
        error = (
            "This activation link has expired. "
            "Please contact the administrator for a new activation link."
        )

    # Password submission
    if request.method == "POST" and not error:

        password = request.POST.get("password", "")
        confirm_password = request.POST.get(
            "confirm_password",
            "",
        )

        if len(password) < 8:
            error = "Password must contain at least 8 characters."

        elif password != confirm_password:
            error = "Password and confirmation password do not match."

        else:
            member.user.set_password(password)
            member.user.save(
                update_fields=["password"]
            )

            # Invalidate activation token after successful use
            member.activation_token = None
            member.activation_token_created_at = None

            member.save(
                update_fields=[
                    "activation_token",
                    "activation_token_created_at",
                    "updated_at",
                ]
            )

            # Automatically login member
            login(request, member.user)

            return redirect("membership:dashboard")

    return render(
        request,
        "membership/member_set_password.html",
        {
            "member": member,
            "error": error,
            "token": token,
        },
    )


def member_login(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "member_profile"):
            return redirect("membership:dashboard")

    error = ""

    if request.method == "POST":
        member_id = request.POST.get("member_id", "").strip()
        password = request.POST.get("password", "")

        username = member_id.lower()

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            if hasattr(user, "member_profile"):
                login(request, user)
                return redirect("membership:dashboard")

            error = "This account is not connected to a member profile."
        else:
            error = "Invalid Member ID or password."

    return render(
        request,
        "membership/login.html",
        {
            "error": error,
        },
    )


@login_required
def member_logout(request):
    logout(request)
    return redirect("membership:login")


@login_required
def member_dashboard(request):
    member = get_object_or_404(
        Member.objects.select_related("application", "user"),
        user=request.user,
    )

    payments = (
        member.application.payments
        .order_by("-payment_month", "-created_at")
    )

    promotion = (
        member.promotions
        .order_by("-effective_date", "-created_at")
        .first()
    )

    today = timezone.localdate()
    current_month = today.replace(day=1)

    current_month_payment = (
        member.application.payments
        .filter(
            payment_type="monthly",
            payment_month=current_month,
        )
        .order_by("-created_at")
        .first()
    )

    fee_settings = (
        MembershipFeeSettings.objects
        .filter(is_active=True)
        .order_by("-id")
        .first()
    )

    monthly_fee = (
        fee_settings.monthly_fee
        if fee_settings
        else None
    )

    return render(
        request,
        "membership/dashboard.html",
        {
            "member": member,
            "payments": payments,
            "promotion": promotion,

            "effective_status": member.effective_status,
            "effective_status_display": member.effective_status_display,

            "current_month": current_month,
            "current_month_payment": current_month_payment,
            "monthly_fee": monthly_fee,
        },
    )

@login_required
def member_monthly_payment(request):
    member = get_object_or_404(
        Member.objects.select_related("application", "user"),
        user=request.user,
    )

    # Suspended/pending members cannot submit monthly payment requests.
    if member.status in ["suspended", "pending"]:
        return render(
            request,
            "membership/payment.html",
            {
                "member": member,
                "error": (
                    "Your membership is not eligible for monthly "
                    "payment at this time."
                ),
            },
        )

    today = timezone.localdate()
    current_month = today.replace(day=1)

    # Check whether current month's payment already exists.
    existing_payment = (
        member.application.payments
        .filter(
            payment_type="monthly",
            payment_month=current_month,
            status__in=["pending", "paid"],
        )
        .order_by("-created_at")
        .first()
    )

    if existing_payment:
        return render(
            request,
            "membership/payment.html",
            {
                "member": member,
                "existing_payment": existing_payment,
                "current_month": current_month,
            },
        )

    # Get active monthly fee settings.
    fee_settings = (
        MembershipFeeSettings.objects
        .filter(is_active=True)
        .order_by("-id")
        .first()
    )

    if not fee_settings:
        return render(
            request,
            "membership/payment.html",
            {
                "member": member,
                "error": "Monthly membership fee is not configured yet.",
            },
        )

    if request.method == "POST":
        form = MemberMonthlyPaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)

            # NEVER trust member-submitted amount/month/application.
            payment.application = member.application
            payment.payment_type = "monthly"
            payment.amount = fee_settings.monthly_fee
            payment.payment_month = current_month
            payment.status = "pending"
            payment.save()

            return redirect("membership:payment_success")

    else:
        form = MemberMonthlyPaymentForm(
            initial={
                "amount": fee_settings.monthly_fee,
                "payment_month": current_month,
            }
        )

    return render(
        request,
        "membership/payment.html",
        {
            "member": member,
            "form": form,
            "monthly_fee": fee_settings.monthly_fee,
            "current_month": current_month,
        },
    )


@login_required
def member_payment_success(request):
    member = get_object_or_404(
        Member.objects.select_related("application", "user"),
        user=request.user,
    )

    payment = (
        member.application.payments
        .filter(
            payment_type="monthly",
        )
        .order_by("-created_at")
        .first()
    )

    return render(
        request,
        "membership/payment_success.html",
        {
            "member": member,
            "payment": payment,
        },
    )


@login_required
def member_change_password(request):
    member = get_object_or_404(
        Member.objects.select_related("application", "user"),
        user=request.user,
    )

    error = ""
    success = ""

    if request.method == "POST":
        current_password = request.POST.get("current_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not request.user.check_password(current_password):
            error = "Your current password is incorrect."

        elif len(new_password) < 8:
            error = "New password must contain at least 8 characters."

        elif new_password != confirm_password:
            error = "New password and confirmation password do not match."

        elif current_password == new_password:
            error = "New password must be different from your current password."

        else:
            request.user.set_password(new_password)
            request.user.save()

            # Keep the member logged in after password change.
            from django.contrib.auth import update_session_auth_hash

            update_session_auth_hash(
                request,
                request.user,
            )

            success = "Your password has been changed successfully."

    return render(
        request,
        "membership/change_password.html",
        {
            "member": member,
            "error": error,
            "success": success,
        },
    )


@login_required
def member_profile_edit(request):
    member = get_object_or_404(
        Member.objects.select_related("application", "user"),
        user=request.user,
    )

    application = member.application

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()

        if not full_name:
            error = "Full name is required."

        elif not phone:
            error = "Phone number is required."

        elif not email:
            error = "Email address is required."

        else:
            application.full_name = full_name
            application.phone = phone
            application.email = email
            application.save(
                update_fields=[
                    "full_name",
                    "phone",
                    "email",
                ]
            )

            request.user.first_name = full_name
            request.user.email = email
            request.user.save(
                update_fields=[
                    "first_name",
                    "email",
                ]
            )

            return redirect("membership:dashboard")

    else:
        error = ""

    return render(
        request,
        "membership/profile_edit.html",
        {
            "member": member,
            "application": application,
            "error": error,
        },
    )


@login_required
def member_photo_update(request):
    member = get_object_or_404(
        Member.objects.select_related("application", "user"),
        user=request.user,
    )

    application = member.application

    if request.method == "POST":
        photo = request.FILES.get("photo")

        if not photo:
            error = "Please select a photo."

            return render(
                request,
                "membership/photo_update.html",
                {
                    "member": member,
                    "error": error,
                },
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if photo.content_type not in allowed_types:
            error = "Only JPG, PNG, and WEBP images are allowed."

            return render(
                request,
                "membership/photo_update.html",
                {
                    "member": member,
                    "error": error,
                },
            )

        max_size = 5 * 1024 * 1024

        if photo.size > max_size:
            error = "Photo size must be 5 MB or less."

            return render(
                request,
                "membership/photo_update.html",
                {
                    "member": member,
                    "error": error,
                },
            )

        application.photo = photo
        application.save(
            update_fields=["photo"]
        )

        return redirect("membership:dashboard")

    return render(
        request,
        "membership/photo_update.html",
        {
            "member": member,
        },
    )



def member_password_reset(request):
    if request.method == "POST":
        member_id = request.POST.get(
            "member_id",
            "",
        ).strip()

        member = (
            Member.objects
            .select_related("application", "user")
            .filter(member_id__iexact=member_id)
            .first()
        )

        if (
            member
            and member.user
            and member.application.email
        ):
            user = member.user

            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )

            token = default_token_generator.make_token(
                user
            )

            reset_url = request.build_absolute_uri(
                f"/join-us/password-reset/confirm/"
                f"{uid}/{token}/"
            )

            send_mail(
                subject="ASOK Member Password Reset",
                message=(
                    f"Dear {member.application.full_name},\n\n"
                    f"You requested a password reset for "
                    f"your ASOK Foundation member account.\n\n"
                    f"Use this link to create a new password:\n\n"
                    f"{reset_url}\n\n"
                    f"If you did not request this password reset, "
                    f"you can safely ignore this email.\n\n"
                    f"ASOK Foundation"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    member.application.email
                ],
                fail_silently=False,
            )

        # Always show the same message.
        return redirect(
            "membership:password_reset_done"
        )

    return render(
        request,
        "membership/password_reset.html",
    )


def member_password_reset_done(request):
    return render(
        request,
        "membership/password_reset_done.html",
    )


def member_password_reset_confirm(
    request,
    uidb64,
    token,
):
    try:
        uid = urlsafe_base64_decode(
            uidb64
        ).decode()

        user = User.objects.get(pk=uid)

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
    ):
        user = None

    if (
        user is None
        or not default_token_generator.check_token(
            user,
            token,
        )
    ):
        return render(
            request,
            "membership/password_reset_confirm.html",
            {
                "error": "This password reset link is invalid or has expired.",
            },
        )

    error = ""

    if request.method == "POST":
        password = request.POST.get(
            "password",
            "",
        )

        confirm_password = request.POST.get(
            "confirm_password",
            "",
        )

        if len(password) < 8:
            error = (
                "Password must contain at least "
                "8 characters."
            )

        elif password != confirm_password:
            error = (
                "Password and confirmation "
                "password do not match."
            )

        else:
            user.set_password(password)
            user.save()

            return redirect(
                "membership:login"
            )

    return render(
        request,
        "membership/password_reset_confirm.html",
        {
            "error": error,
        },
    )