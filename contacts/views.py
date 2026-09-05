from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactMessageForm
from core.email_utils import send_admin_notification


def contact_home(request):

    if request.method == "POST":

        form = ContactMessageForm(request.POST)

        if form.is_valid():

            form.save()

            send_admin_notification(
    subject=f"New Contact Message — {contact.name}",
    message=(
        f"Name: {contact.name}\n"
        f"Email: {contact.email}\n"
        f"Phone: {contact.phone}\n\n"
        f"Message:\n{contact.message}"
    ),
)

            messages.success(
                request,
                "Your message has been sent successfully. "
                "Our team will get back to you soon.",
            )

            return redirect("contacts:success")

    else:

        form = ContactMessageForm()

    return render(
        request,
        "contacts/home.html",
        {
            "form": form,
        },
    )


def contact_success(request):

    return render(
        request,
        "contacts/success.html",
    )