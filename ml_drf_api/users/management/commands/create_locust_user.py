import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates a regular user for locust to authenticate"

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            user = User.objects.get(username="locust")
            logging.info("User 'locust' found. Skipping.")
        except User.DoesNotExist:
            user = User.objects.create_user("locust", "", "locust", is_superuser=False)
            logging.info("New user 'locust' created.")
            user.save()
