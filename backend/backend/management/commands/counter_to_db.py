from django.core.management.base import BaseCommand, CommandError
from backend.models import Telemetry, Database
from django.utils import timezone
import datetime
import time


class Command(BaseCommand):
    help = "Generates a sine wave directly to the database through the ORB"

    def handle(self, *args, **options):
        db, _ = Database.objects.get_or_create(default=True)

        counter = 0
        while True:
            counter += 1
            Telemetry.objects.create(database=db, data={"counter": counter})
