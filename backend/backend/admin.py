from django.contrib import admin
from .models import Database, Telemetry


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ["name", "default"]


class TelemetryAdmin(admin.ModelAdmin):

    list_display = ["time"]
    list_filter = ["database"]


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Telemetry, TelemetryAdmin)
