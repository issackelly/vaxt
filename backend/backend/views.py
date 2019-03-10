from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Database, Telemetry

from .influx_adapter import influx_write_string_to_vaxt


@csrf_exempt
def write_influxdb(request):
    if request.GET.get("db"):
        database, _ = Database.objects.get_or_create(name=request.GET.get("db"))
    else:
        database = Database.objects.get_or_create(
            default=True, defaults={"name": "default"}
        )

    try:
        influx_write_string_to_vaxt(database, request.body.decode("utf-8"))
        return HttpResponse("", status=204)
    except Exception as exc:
        print(request.body.decode('utf-8'))
        raise(exc)
        return HttpResponse("error", status=400)
