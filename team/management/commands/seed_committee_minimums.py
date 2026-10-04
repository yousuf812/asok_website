from django.core.management.base import BaseCommand

from team.models import CommitteeMinimum, CommitteeType


class Command(BaseCommand):
    help = "Create or update default committee minimum member requirements."

    def handle(self, *args, **options):

        minimums = {
            CommitteeType.CENTRAL: 0,
            CommitteeType.DIVISION: 101,
            CommitteeType.DISTRICT: 101,
            CommitteeType.METROPOLITAN: 101,
            CommitteeType.THANA_UPAZILA: 51,
            CommitteeType.MUNICIPALITY: 51,
            CommitteeType.UNION_WARD: 31,
        }

        for committee_type, minimum_members in minimums.items():

            obj, created = CommitteeMinimum.objects.update_or_create(
                committee_type=committee_type,
                defaults={
                    "minimum_members": minimum_members,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {obj.get_committee_type_display()} "
                        f"= {minimum_members}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Updated: {obj.get_committee_type_display()} "
                        f"= {minimum_members}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Committee minimum requirements seeded successfully."
            )
        )