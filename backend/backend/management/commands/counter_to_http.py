from django.core.management.base import BaseCommand, CommandError
from backend.models import Telemetry, Database
from django.utils import timezone
import requests
import datetime
import time


class Command(BaseCommand):
    help = "Generates a sine wave directly to the database through the ORB"

    def handle(self, *args, **options):
        counter = 0
        while True:
            counter += 1
            requests.post(
                "http://localhost:8000/write?db=default",
                data=f"""counter_test counter={counter}""",
            )
