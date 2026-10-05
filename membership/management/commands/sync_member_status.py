from django.core.management.base import BaseCommand
from django.utils import timezone

from membership.models import Member


class Command(BaseCommand):
    help = "Sync member active/inactive status based on current month's membership payment."

    def handle(self, *args, **options):
        today = timezone.localdate()

        members = Member.objects.select_related("application").all()

        active_count = 0
        inactive_count = 0
        skipped_count = 0

        for member in members:

            # Do not change suspended members.
            if member.status == "suspended":
                skipped_count += 1
                continue

            # Pending members remain pending.
            if member.status == "pending":
                skipped_count += 1
                continue

            # Registration fee must be paid.
            registration_paid = member.application.payments.filter(
                payment_type="registration",
                status="paid",
            ).exists()

            if not registration_paid:
                if member.status != "inactive":
                    member.status = "inactive"
                    member.save(update_fields=["status", "updated_at"])

                inactive_count += 1
                continue

            # Check current month's monthly payment.
            monthly_paid = member.application.payments.filter(
                payment_type="monthly",
                status="paid",
                payment_month__year=today.year,
                payment_month__month=today.month,
            ).exists()

            if monthly_paid:
                if member.status != "active":
                    member.status = "active"

                    if not member.activation_date:
                        member.activation_date = today

                    member.save(
                        update_fields=[
                            "status",
                            "activation_date",
                            "updated_at",
                        ]
                    )

                active_count += 1

            else:
                if member.status != "inactive":
                    member.status = "inactive"
                    member.save(update_fields=["status", "updated_at"])

                inactive_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Member status sync completed. "
                f"Active: {active_count}, "
                f"Inactive: {inactive_count}, "
                f"Skipped: {skipped_count}"
            )
        )