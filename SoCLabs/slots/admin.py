from django.contrib import admin
from .models import(
    TimeSchedule,
    TimeSlot,
    TimeConfig,
    Board,
    IPAddress,
    StartDay
)

admin.site.register(TimeConfig)
admin.site.register(TimeSlot)
admin.site.register(TimeSchedule)
admin.site.register(Board)
admin.site.register(IPAddress)
admin.site.register(StartDay)