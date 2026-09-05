from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import MembershipApplicationForm
from core.email_utils import send_admin_notification


def membership_home(request):

    if request.method == "POST":

        form = MembershipApplicationForm(request.POST)

        if form.is_valid():

            application = form.save()

            send_admin_notification(
                subject=f"New Membership Application — {application.name}",
                message=(
                    f"Name: {application.name}\n"
                    f"Email: {application.email}\n"
                    f"Phone: {application.phone}\n\n"
                    f"Message:\n{application.message}"
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