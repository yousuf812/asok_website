from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ComplaintForm
from core.email_utils import send_admin_notification


def complaint_home(request):

    if request.method == "POST":

        form = ComplaintForm(request.POST)

        if form.is_valid():

            complaint = form.save()

            send_admin_notification(
    subject=f"New Complaint — {complaint.complaint_id}",
    message=(
        f"Complaint ID: {complaint.complaint_id}\n"
        f"Name: {complaint.name}\n"
        f"Email: {complaint.email}\n"
        f"Phone: {complaint.phone}\n\n"
        f"Category: {complaint.category}\n"
        f"Description:\n{complaint.description}"
    ),
)

            request.session["complaint_id"] = (
                complaint.complaint_id
            )

            messages.success(
                request,
                "Your complaint has been submitted successfully."
            )

            return redirect(
                "complaints:success"
            )

    else:

        form = ComplaintForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "complaints/home.html",
        context
    )


def complaint_success(request):

    complaint_id = request.session.get(
        "complaint_id"
    )

    context = {
        "complaint_id": complaint_id,
    }

    return render(
        request,
        "complaints/success.html",
        context
    )