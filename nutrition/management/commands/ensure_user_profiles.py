from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from nutrition.models import UserProfile

class Command(BaseCommand):
    help = 'Ensures all users have a user profile'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Profile created for {user.username}'))



