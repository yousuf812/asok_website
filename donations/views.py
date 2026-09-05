from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from .models import Donation
from .forms import DonationForm, DonationLookupForm

from core.email_utils import send_admin_notification


def donation_home(request):

    if request.method == "POST":
        form = DonationForm(request.POST)

        if form.is_valid():
            donation = form.save()

            send_admin_notification(
                subject=f"New Donation — {donation.reference_number}",
                message=(
                    f"Reference Number: {donation.reference_number}\n"
                    f"Name: {donation.name}\n"
                    f"Email: {donation.email}\n"
                    f"Phone: {donation.phone}\n"
                    f"Amount: {donation.amount}\n"
                    f"Payment Method: {donation.payment_method}\n"
                    f"Purpose: {donation.purpose}\n\n"
                    f"Status: {donation.status}"
                ),
            )

            request.session["donation_reference"] = (
                donation.reference_number
            )

            messages.success(
                request,
                "Your donation information has been submitted successfully.",
            )

            return redirect("donations:success")

    else:
        form = DonationForm()

    return render(
        request,
        "donations/home.html",
        {"form": form},
    )


def donation_success(request):

    reference_number = request.session.get(
        "donation_reference"
    )

    return render(
        request,
        "donations/success.html",
        {"reference_number": reference_number},
    )


@staff_member_required
def donation_dashboard(request):

    total_donations = Donation.objects.count()

    pending_donations = Donation.objects.filter(
        status="pending"
    ).count()

    verified_donations = Donation.objects.filter(
        status="verified"
    ).count()

    failed_donations = Donation.objects.filter(
        status="failed"
    ).count()

    cancelled_donations = Donation.objects.filter(
        status="cancelled"
    ).count()

    verified_amount = (
        Donation.objects
        .filter(status="verified")
        .aggregate(total=Sum("amount"))
        ["total"]
    ) or 0

    recent_donations = Donation.objects.all()[:10]

    context = {
        "total_donations": total_donations,
        "pending_donations": pending_donations,
        "verified_donations": verified_donations,
        "failed_donations": failed_donations,
        "cancelled_donations": cancelled_donations,
        "verified_amount": verified_amount,
        "recent_donations": recent_donations,
    }

    return render(
        request,
        "donations/dashboard.html",
        context,
    )


def donation_lookup(request):

    donation = None
    form = DonationLookupForm()

    if request.method == "POST":

        form = DonationLookupForm(request.POST)

        if form.is_valid():

            reference_number = form.cleaned_data[
                "reference_number"
            ]

            donation = (
                Donation.objects
                .filter(
                    reference_number=reference_number
                )
                .first()
            )

            if donation is None:
                form.add_error(
                    "reference_number",
                    "No donation found with this reference number.",
                )

    return render(
        request,
        "donations/lookup.html",
        {
            "form": form,
            "donation": donation,
        },
    )