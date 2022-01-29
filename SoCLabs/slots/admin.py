from django.contrib import admin
from .models import(
    TimeSchedule,
    TimeSlot
)

admin.site.register(TimeSlot)
admin.site.register(TimeSchedule)