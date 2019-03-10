from django.test import TestCase
from .models import Database, Telemetry
from .influx_adapter import influx_write_string_to_vaxt


class InfluxWriteTest(TestCase):
    def setUp(self):
        self.db = Database.objects.create(name="default", default=True)

    def test_timestamp(self):
        mar_10_2019_2000 = 1_552_248_013
        # Specify the time
        errors = influx_write_string_to_vaxt(
            self.db, f""""metric old=1 {mar_10_2019_2000}001067000"""
        )
        self.assertEqual(errors, [])
        self.assertEqual(Telemetry.objects.count(), 1)

        tm = Telemetry.objects.first()
        self.assertEqual(tm.time.year, 2019)
        self.assertEqual(tm.time.month, 3)
        self.assertEqual(tm.time.day, 10)
        self.assertEqual(tm.time.hour, 20)
        self.assertEqual(tm.time.minute, 0)
        self.assertEqual(tm.time.second, 13)
        self.assertEqual(tm.time.microsecond, 1067)

    def test_basic(self):
        # Add one
        influx_write_string_to_vaxt(self.db, """"metric key=1""")
        self.assertEqual(Telemetry.objects.count(), 1)

        # Add another
        influx_write_string_to_vaxt(self.db, """"metric key=1,another=2,more=3""")
        self.assertEqual(Telemetry.objects.count(), 2)

        tm = Telemetry.objects.order_by("-time").first()
        self.assertEqual(tm.data, {"key": 1, "another": 2, "more": 3})

        # Specify the time
        influx_write_string_to_vaxt(self.db, """"metric old=1 1""")
        self.assertEqual(Telemetry.objects.count(), 3)

        tm = Telemetry.objects.order_by("time").first()
        self.assertEqual(tm.time.year, 1970)

        # Specify tags
        influx_write_string_to_vaxt(self.db, """"metric,some=extra,data=here key=1""")
        self.assertEqual(Telemetry.objects.count(), 4)

        tm = Telemetry.objects.order_by("-time").first()
        self.assertEqual(tm.tags, {"some": "extra", "data": "here"})

        # Multi line multi-point
        # Specify tags
        influx_write_string_to_vaxt(
            self.db,
            """"metric key=1 another=2 more=3
metric key=1 another=2 more=3
metric key=1 another=2 more=3""",
        )
        self.assertEqual(Telemetry.objects.count(), 7)
