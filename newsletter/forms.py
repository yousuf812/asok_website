from django import forms
from .models import Subscriber


class NewsletterSubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        fields = ["email"]

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter your email address",
                    "autocomplete": "email",
                }
            ),
        }

        labels = {
            "email": "Email Address",
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if Subscriber.objects.filter(
            email=email,
            is_active=True,
        ).exists():
            raise forms.ValidationError(
                "This email is already subscribed to our newsletter."
            )

        return email