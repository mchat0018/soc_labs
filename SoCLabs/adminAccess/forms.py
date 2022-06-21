from pyexpat import model
from django import forms
from courses.models import Course,Lab
from slots.models import TimeConfig,TimeSchedule,TimeSlot,IPAddress
from datetime import datetime

class BoardSelectForm(forms.ModelForm):

    class Meta:
        model = IPAddress
        fields = ['board_name']


daysList = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days = []
for i in range(datetime.today().weekday(), 7):
    days.append((daysList[i], daysList[i]))
for i in range(0, datetime.today().weekday()):
    days.append((daysList[i], daysList[i]))

hrs = [(str(i), str(i)) for i in range(10, 19)]

mins = [
    ('00', '00'),
    ('15', '15'),
    ('30', '30'),
    ('45', '45'),
]


class ConfigsCRUD(forms.ModelForm):

    class Meta:
        model = IPAddress
        fields = '__all__'

    day = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
                "placeholder": "Select Day...",
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

    duration = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    slot_limit = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control",
            }
        ),
    )

    course = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
            }, choices=[]
        ),
    )

    def __init__(self, coursenames=None, *args, **kwargs):
        super(ConfigsCRUD, self).__init__(*args, **kwargs)
        if coursenames:
            self.fields['course'].choices = coursenames