import json
from pathlib import Path

from django.core.management.base import BaseCommand

from team.models import (
    Division,
    District,
    Upazila,
    Municipality,
    UnionWard,
)


class Command(BaseCommand):
    help = "Import Bangladesh administrative location data."

    def handle(self, *args, **options):
        data_file = (
            Path(__file__).resolve().parent.parent.parent
            / "data"
            / "bangladesh-geo.json"
        )

        if not data_file.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"Data file not found: {data_file}"
                )
            )
            return

        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        division_count = 0
        district_count = 0
        upazila_count = 0
        municipality_count = 0
        union_count = 0

        for division_data in data:
            division, _ = Division.objects.update_or_create(
                name=division_data["bn_name"],
                defaults={
                    "name": division_data["bn_name"],
                },
            )

            division_count += 1

            for district_data in division_data.get("districts", []):
                district, _ = District.objects.update_or_create(
                    division=division,
                    name=district_data["bn_name"],
                    defaults={
                        "name": district_data["bn_name"],
                    },
                )

                district_count += 1

                for upazila_data in district_data.get("upazilas", []):
                    upazila, _ = Upazila.objects.update_or_create(
                        district=district,
                        name=upazila_data["bn_name"],
                        defaults={
                            "name": upazila_data["bn_name"],
                        },
                    )

                    upazila_count += 1

                    for pourashava_data in upazila_data.get(
                        "pourashavas", []
                    ):
                        Municipality.objects.update_or_create(
                            upazila=upazila,
                            name=pourashava_data["bn_name"],
                            defaults={
                                "name": pourashava_data["bn_name"],
                            },
                        )

                        municipality_count += 1

                    for union_data in upazila_data.get(
                        "unions", []
                    ):
                        UnionWard.objects.update_or_create(
                            upazila=upazila,
                            name=union_data["bn_name"],
                            defaults={
                                "name": union_data["bn_name"],
                            },
                        )

                        union_count += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Bangladesh location data imported successfully!"
            )
        )

        self.stdout.write(
            f"Divisions: {division_count}"
        )
        self.stdout.write(
            f"Districts: {district_count}"
        )
        self.stdout.write(
            f"Upazilas: {upazila_count}"
        )
        self.stdout.write(
            f"Municipalities: {municipality_count}"
        )
        self.stdout.write(
            f"Unions/Wards: {union_count}"
        )