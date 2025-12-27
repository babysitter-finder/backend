"""Management command to seed test services for development."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand
from django.utils import timezone

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

        # Use local timezone (America/Mexico_City = UTC-6)
        local_tz = ZoneInfo("America/Mexico_City")
        now = timezone.now()

        # Service 1: Starting in 30 minutes (within 90-min window)
        scheduled_start_1 = now + timedelta(minutes=30)
        service1 = Service.objects.create(
            user_client=client,
            user_bbs=babysitter,
            date=today,
            shift="morning",
            scheduled_start=scheduled_start_1,
            address=client_user.address or "123 Test Street",
            lat=client_user.lat,
            long=client_user.long,
            count_children=2,
            special_cares="No allergies",
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Created Service #{service1.id}: {today} morning - starts in 30 mins (ON_MY_WAY ENABLED)"
        ))

        # Service 2: Tomorrow afternoon (beyond 90-min window)
        scheduled_start_2 = datetime(
            tomorrow.year, tomorrow.month, tomorrow.day, 14, 0, 0,
            tzinfo=local_tz
        )
        service2 = Service.objects.create(
            user_client=client,
            user_bbs=babysitter,
            date=tomorrow,
            shift="afternoon",
            scheduled_start=scheduled_start_2,
            address=client_user.address or "123 Test Street",
            lat=client_user.lat,
            long=client_user.long,
            count_children=1,
            special_cares="Needs bedtime story",
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Created Service #{service2.id}: {tomorrow} 2:00 PM (ON_MY_WAY DISABLED)"
        ))

        # Service 3: Next week evening (beyond 90-min window)
        scheduled_start_3 = datetime(
            next_week.year, next_week.month, next_week.day, 18, 0, 0,
            tzinfo=local_tz
        )
        service3 = Service.objects.create(
            user_client=client,
            user_bbs=babysitter,
            date=next_week,
            shift="evening",
            scheduled_start=scheduled_start_3,
            address=client_user.address or "123 Test Street",
            lat=client_user.lat,
            long=client_user.long,
            count_children=3,
            special_cares="One child needs medication at 8pm",
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Created Service #{service3.id}: {next_week} 6:00 PM (ON_MY_WAY DISABLED)"
        ))

        self.stdout.write(self.style.SUCCESS("\n=== Test Services Ready ==="))
        self.stdout.write(f"  Service #{service1.id}: {scheduled_start_1.astimezone(local_tz)} - ON_MY_WAY ENABLED")
        self.stdout.write(f"  Service #{service2.id}: {scheduled_start_2} - ON_MY_WAY DISABLED")
        self.stdout.write(f"  Service #{service3.id}: {scheduled_start_3} - ON_MY_WAY DISABLED")
        self.stdout.write("\nLogin as testbabysitter / testpass123 to test on_my_way endpoint")
