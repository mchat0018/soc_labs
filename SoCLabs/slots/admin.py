from django.contrib import admin
from .models import(
    TimeSchedule,
    TimeSlot,
    TimeConfig
)

admin.site.register(TimeConfig)
admin.site.register(TimeSlot)
admin.site.register(TimeSchedule)