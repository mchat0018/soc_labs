from django.contrib import admin
from .models import(
    TimeSchedule,
    TimeSlot,
    TimeConfig,
    Board,
    IPAddress
)

admin.site.register(TimeConfig)
admin.site.register(TimeSlot)
admin.site.register(TimeSchedule)
admin.site.register(Board)
admin.site.register(IPAddress)