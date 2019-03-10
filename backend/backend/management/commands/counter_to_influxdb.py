from django.core.management.base import BaseCommand, CommandError
from influxdb import InfluxDBClient


class Command(BaseCommand):
    help = "Generates a sine wave directly to the database through the ORB"

    def handle(self, *args, **options):
        client = InfluxDBClient("localhost", 8000, "", "", "some_data")

        counter = 0
        while True:
            counter += 1
            client.write_points(
                [
                    {
                        "measurement": "conter",
                        "tags": {"source": "influxclient"},
                        "fields": {"counter": counter, "somebool": False, "othertrue": True, "afloat": float(counter / 10)},
                    }
                ]
            )
