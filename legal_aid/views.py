from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import LegalAidRequestForm
from core.email_utils import send_admin_notification


def legal_aid_home(request):

    if request.method == "POST":

        form = LegalAidRequestForm(request.POST)

        if form.is_valid():

            legal_request = form.save()

            send_admin_notification(
                subject=f"New Legal Aid Request — {legal_request.reference_number}",
                message=(
                    f"Reference Number: {legal_request.reference_number}\n"
                    f"Name: {legal_request.name}\n"
                    f"Email: {legal_request.email}\n"
                    f"Phone: {legal_request.phone}\n\n"
                    f"Category: {legal_request.category}\n"
                    f"Message:\n{legal_request.description}"
                ),
            )

            request.session["legal_aid_reference"] = (
                legal_request.reference_number
            )

            messages.success(
                request,
                (
                    "Your legal assistance request has been "
                    "submitted successfully."
                ),
            )

            return redirect(
                "legal_aid:success"
            )

    else:

        form = LegalAidRequestForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "legal_aid/home.html",
        context
    )


def legal_aid_success(request):

    reference_number = request.session.get(
        "legal_aid_reference"
    )

    context = {
        "reference_number": reference_number,
    }

    return render(
        request,
        "legal_aid/success.html",
        context
    )