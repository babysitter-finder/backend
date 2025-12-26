"""Management command to seed test services for development."""

from datetime import date, timedelta

from django.core.management.base import BaseCommand

from hisitter.services.models import Service
from hisitter.users.models import User, Client, Babysitter


class Command(BaseCommand):
    help = "Create test services for frontend testing"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Delete all existing services before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write("Seeding test services...")

        # Clean existing services if --clean flag is passed
        if options['clean']:
            deleted_count, _ = Service.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing services"))

        # Get or verify test users exist
        try:
            client_user = User.objects.get(username="testclient")
            client = Client.objects.get(user_client=client_user)
        except (User.DoesNotExist, Client.DoesNotExist):
            self.stdout.write(self.style.ERROR(
                "testclient not found. Run 'python manage.py seed_users' first."
            ))
            return

        try:
            bbs_user = User.objects.get(username="testbabysitter")
            babysitter = Babysitter.objects.get(user_bbs=bbs_user)
        except (User.DoesNotExist, Babysitter.DoesNotExist):
            self.stdout.write(self.style.ERROR(
                "testbabysitter not found. Run 'python manage.py seed_users' first."
            ))
            return

        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)

        # Service 1: Today morning
        service1 = Service.objects.create(
            user_client=client,
            user_bbs=babysitter,
            date=today,
            shift="morning",
            address=client_user.address or "123 Test Street",
            lat=client_user.lat,
            long=client_user.long,
            count_children=2,
            special_cares="No allergies",
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Created Service #{service1.id}: {today} morning"
        ))

        # Service 2: Tomorrow afternoon
        service2 = Service.objects.create(
            user_client=client,
            user_bbs=babysitter,
            date=tomorrow,
            shift="afternoon",
            address=client_user.address or "123 Test Street",
            lat=client_user.lat,
            long=client_user.long,
            count_children=1,
            special_cares="Needs bedtime story",
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Created Service #{service2.id}: {tomorrow} afternoon"
        ))

        # Service 3: Next week evening
        service3 = Service.objects.create(
            user_client=client,
            user_bbs=babysitter,
            date=next_week,
            shift="evening",
            address=client_user.address or "123 Test Street",
            lat=client_user.lat,
            long=client_user.long,
            count_children=3,
            special_cares="One child needs medication at 8pm",
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Created Service #{service3.id}: {next_week} evening"
        ))

        self.stdout.write(self.style.SUCCESS("\n=== Test Services Ready ==="))
        self.stdout.write(f"  Service #{service1.id}: {today} morning")
        self.stdout.write(f"  Service #{service2.id}: {tomorrow} afternoon")
        self.stdout.write(f"  Service #{service3.id}: {next_week} evening")
        self.stdout.write("\nLogin as testbabysitter / testpass123 to test on_my_way endpoint")
