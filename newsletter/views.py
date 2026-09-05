from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import NewsletterSubscriptionForm


def subscribe(request):

    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)

        if form.is_valid():
            subscriber = form.save()

            messages.success(
                request,
                "Thank you! You have successfully subscribed to our newsletter.",
            )

            return redirect("newsletter:subscribe")

    else:
        form = NewsletterSubscriptionForm()

    return render(
        request,
        "newsletter/subscribe.html",
        {
            "form": form,
        },
    )