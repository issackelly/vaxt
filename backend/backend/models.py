from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
import datetime


class Database(models.Model):
    name = models.SlugField(primary_key=True, unique=True)
    default = models.BooleanField(default=False)

    # TODO single source default

    class Meta:
        db_table = "telemetry_dbs"


def _get_default_db():
    try:
        return Database.objects.get(default=True)
    except Database.DoesNotExist:
        return Database.objects.create(default=True)


class Telemetry(models.Model):
    database = models.ForeignKey(
        Database, default=_get_default_db, null=True, on_delete=models.SET_NULL
    )
    metric_name = models.CharField(
        blank=True, default="'", db_index=True, max_length=64
    )
    time = models.DateTimeField(primary_key=True, default=timezone.now)
    tags = JSONField(blank=True, null=True)
    data = JSONField(blank=True, null=True)

    class Meta:
        db_table = "telemetry"
        unique_together = ["database", "time", "metric_name", "tags"]
