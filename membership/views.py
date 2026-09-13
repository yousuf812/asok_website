from django.contrib import messages

from .models import MembershipPayment, MembershipFeeSettings
from .forms import MembershipApplicationForm
from core.email_utils import send_admin_notification
import base64
from io import BytesIO

import qrcode

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Member


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
                    f"Email: {application.email}\n"
                    f"Phone: {application.phone}\n"
                    f"Membership Type: "
                    f"{application.get_membership_type_display()}\n"
                    f"NID: "
                    f"{application.nid_number or 'Not provided'}\n"
                    f"Birth Registration: "
                    f"{application.birth_registration_number or 'Not provided'}\n\n"
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


from django.shortcuts import get_object_or_404, render

from .models import Member


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