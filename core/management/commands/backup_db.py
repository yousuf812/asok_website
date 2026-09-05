from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a backup of the database"

    def handle(self, *args, **options):
        base_dir = Path.cwd()
        backup_file = base_dir / "backup.json"

        self.stdout.write("Creating database backup...")

        with open(backup_file, "w", encoding="utf-8") as file:
            call_command(
                "dumpdata",
                indent=2,
                stdout=file,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Backup created successfully: {backup_file}"
            )
        )