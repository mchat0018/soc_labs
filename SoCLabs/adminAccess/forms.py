from pyexpat import model
from random import choices
from django import forms
from django.core.validators import MaxValueValidator,MinValueValidator
from courses.models import Course,Lab
from slots.models import TimeConfig,TimeSchedule,TimeSlot,IPAddress
from datetime import datetime

daysList = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days = []
for i in range(datetime.today().weekday(), 7):
    days.append((daysList[i], daysList[i]))
for i in range(0, datetime.today().weekday()):
    days.append((daysList[i], daysList[i]))

hrs = [(str(i).zfill(2), str(i).zfill(2)) for i in range(0, 24)]

mins = [
    ('00', '00'),
    ('15', '15'),
    ('30', '30'),
    ('45', '45'),
]

dur = [
    (15,15),
    (30,30),
    (45,45),
    (60,60)
]

class ConfigsCRUD(forms.ModelForm):

    class Meta:
        model = TimeConfig
        fields = [
                'day','start_time_hours','start_time_minutes',
                'end_time_hours','end_time_minutes',
                'duration', 'slot_limit'
        ]

    day = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
            },
            choices=days
        ),
    )

    start_time_hours = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
            },
            choices=hrs
        ),
    )

    start_time_minutes = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
            },
            choices=mins
        ),
    )

    end_time_hours = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
            },
            choices=hrs
        ),
    )

    end_time_minutes = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
            },
            choices=mins
        ),
    )

    duration = forms.IntegerField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
            },
            choices=dur
        ),
    )

    slot_limit = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
            }
        ),
        validators=[
            MinValueValidator(1),
        ]
    )