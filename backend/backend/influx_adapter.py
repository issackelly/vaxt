from .models import Database, Telemetry
from django.utils import timezone
import datetime
import time


class InfluxParseException(Exception):
    pass


def influx_write_string_to_vaxt(database, string):
    """
    ! WARNING
    This implementation rounds to microseconds

    :param string: https://docs.influxdata.com/influxdb/v1.7/write_protocols/line_protocol_reference/
    :return: list of errors in parsing
    """
    created_count = 0

    errors = []

    # Each line is one point
    for index, line in enumerate(string.split("\n")):
        if not line:
            continue
        try:
            measurement_and_tags, values, timestamp = line.split(" ")
        except ValueError:
            try:
                measurement_and_tags, values = line.split(" ")
                timestamp = ""
            except Exception as exc:
                errors.append(exc)
                continue

        try:
            metric_name, tag_string = measurement_and_tags.split(",", 1)
        except ValueError:
            metric_name = measurement_and_tags
            tag_string = ""
        tags = {}

        if tag_string:
            for kvpair in tag_string.split(","):
                key, value = kvpair.split("=")
                tags[key] = value

        #TODO VALUES ARE , separated not ' ' separated
        values = values.split(",")

        # Is the last element a metric or a timestamp?
        if timestamp == "":
            metric_time = timezone.now()
        else:
            # Assume the last element is a Unix nanosecond timestamp in UTC time
            try:
                ns_time = int(timestamp)
            except ValueError:
                errors.append(
                    InfluxParseException(
                        f"Tried to parse a timestamp but could not. {values[-1]} on line {index}"
                    )
                )
                continue

            values = values[:-1]

            seconds, nanoseconds = divmod(ns_time, 1e9)
            microseconds, _ = divmod(nanoseconds, 1000)
            metric_time = datetime.datetime.fromtimestamp(
                seconds, datetime.timezone.utc
            ) + datetime.timedelta(microseconds=microseconds)

        telem, _ = Telemetry.objects.get_or_create(
            tags=tags, time=metric_time, metric_name=metric_name, database=database
        )
        if not telem.data:
            telem.data = {}

        for kvpair in values:
            key, value = kvpair.split("=")
            if value.endswith('i'):
                try:
                    telem.data[key] = int(value.strip())
                except ValueError:
                    telem.data[key] = value
            elif value.endswith('f'):
                try:
                    telem.data[key] = float(value.strip())
                except ValueError:
                    telem.data[key] = value
            elif value == "True":
                telem.data[key] = True
            elif value == "False":
                telem.data[key] = False
            else:
                try:
                    telem.data[key] = float(value.strip())
                except ValueError:
                    telem.data[key] = value

        telem.save()

    if errors:
        raise errors[0]

    return errors
