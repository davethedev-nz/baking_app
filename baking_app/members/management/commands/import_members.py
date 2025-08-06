import csv
from django.core.management.base import BaseCommand
from members.models import Member

class Command(BaseCommand):
    help = 'Import members from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        created_count = 0
        skipped_count = 0

        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    business_name = row.get('*ContactName')
                    membership_number = row.get('AccountNumber')
                    email = row.get('EmailAddress')

                    if not (business_name and membership_number and email):
                        self.stdout.write(self.style.WARNING(f'Skipping row: {row} — missing fields'))
                        skipped_count += 1
                        continue

                    member, created = Member.objects.get_or_create(
                        email=email,
                        business_name=business_name,
                        membership_number=membership_number
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created member: {business_name}'))
                        created_count += 1
                    else:
                        self.stdout.write(self.style.NOTICE(f'Skipped (already exists): {business_name}'))
                        skipped_count += 1

            self.stdout.write(self.style.SUCCESS(f'\n✅ Import complete: {created_count} added, {skipped_count} skipped'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
