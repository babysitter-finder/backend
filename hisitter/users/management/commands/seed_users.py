"""Management command to seed test users for development."""

from decimal import Decimal

from django.core.management.base import BaseCommand

from hisitter.users.models import User, Client, Babysitter, Availability


class Command(BaseCommand):
    help = "Create verified test users for each role (client and babysitter)"

    def handle(self, *args, **options):
        self.stdout.write("Seeding test users...")

        # Create or update verified client user
        client_user, created = User.objects.get_or_create(
            username="testclient",
            defaults={
                "email": "client@test.com",
                "first_name": "Test",
                "last_name": "Client",
                "phone_number": "5551234567",
                "birthdate": "1990-01-15",
                "address": "123 Client Street, New York, NY",
                "genre": "Male",
                "is_verified": True,
            }
        )
        # Always reset password and verify (handles existing users)
        client_user.email = "client@test.com"
        client_user.is_verified = True
        client_user.set_password("testpass123")
        client_user.save()
        if created:
            Client.objects.create(user_client=client_user)
            self.stdout.write(self.style.SUCCESS(
                f"Created client: testclient / testpass123"
            ))
        else:
            if not hasattr(client_user, 'user_client'):
                Client.objects.create(user_client=client_user)
            self.stdout.write(self.style.SUCCESS(
                f"Updated client: testclient / testpass123"
            ))

        # Create or update verified babysitter user
        babysitter_user, created = User.objects.get_or_create(
            username="testbabysitter",
            defaults={
                "email": "babysitter@test.com",
                "first_name": "Test",
                "last_name": "Babysitter",
                "phone_number": "5559876543",
                "birthdate": "1985-05-20",
                "address": "456 Babysitter Ave, Los Angeles, CA",
                "genre": "Female",
                "is_verified": True,
            }
        )
        # Always reset password and verify (handles existing users)
        babysitter_user.email = "babysitter@test.com"
        babysitter_user.is_verified = True
        babysitter_user.set_password("testpass123")
        babysitter_user.save()
        if created:
            babysitter = Babysitter.objects.create(
                user_bbs=babysitter_user,
                education_degree="Early Childhood Education",
                about_me="Experienced babysitter with 5+ years of experience.",
                cost_of_service=Decimal("25.00")
            )
            # Add availability for all weekdays
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                for shift in ["morning", "afternoon"]:
                    Availability.objects.create(bbs=babysitter, day=day, shift=shift)
            self.stdout.write(self.style.SUCCESS(
                f"Created babysitter: testbabysitter / testpass123"
            ))
        else:
            if not hasattr(babysitter_user, 'user_bbs'):
                babysitter = Babysitter.objects.create(
                    user_bbs=babysitter_user,
                    education_degree="Early Childhood Education",
                    about_me="Experienced babysitter with 5+ years of experience.",
                    cost_of_service=Decimal("25.00")
                )
                for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                    for shift in ["morning", "afternoon"]:
                        Availability.objects.create(bbs=babysitter, day=day, shift=shift)
            self.stdout.write(self.style.SUCCESS(
                f"Updated babysitter: testbabysitter / testpass123"
            ))

        self.stdout.write(self.style.SUCCESS("\nTest users ready:"))
        self.stdout.write("  Client:     testclient / testpass123 (client@test.com)")
        self.stdout.write("  Babysitter: testbabysitter / testpass123 (babysitter@test.com)")
