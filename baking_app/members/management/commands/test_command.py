from django.core.management.base import BaseCommand
from members.models import Member


class Command(BaseCommand):
    help = 'Prints all member emails or filters by a given email.'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Filter by email')

    def handle(self, *args, **options):
        email = options.get('email')

        if email:
            try:
                member = Member.objects.get(email=email)
                self.stdout.write(self.style.SUCCESS(f"Found: {member.email}"))
            except Member.DoesNotExist:
                self.stderr.write(self.style.ERROR("No member found with that email."))
        else:
            self.stdout.write("All member emails:")
            for member in Member.objects.all():
                self.stdout.write(f"- {member.email}")
