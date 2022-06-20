from django import forms
from slots.models import TimeConfig
from datetime import datetime

daysList = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
days = []
for i in range(datetime.today().weekday(),7):
    days.append((daysList[i],daysList[i]))
for i in range(0,datetime.today().weekday()):
    days.append((daysList[i],daysList[i]))

hrs = [(str(i), str(i)) for i in range(10,19)]

mins = [
    ('00', '00'),
    ('15', '15'),
    ('30', '30'),
    ('45', '45'),
]

class TimeConfigFrm(forms.ModelForm):
    class Meta:
        model = TimeConfig
        fields = "__all__"

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
                "placeholder": "Select Day...",
                "size": 4,
            },
            choices=hrs
        ),
    )

    start_time_minutes = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
                "placeholder": "Select Day...",
                "size": 4,
            },
            choices=mins
        ),
    )

    end_time_hours = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
                "placeholder": "Select Day...",
                "size": 4,
            },
            choices=hrs
        ),
    )

    end_time_minutes = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
                "placeholder": "Select Day...",
                "size": 4,
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

    # no_of_boards = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #         }
    #     ),
    # )

    no_of_boards = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control form-select",
            },choices=[]
        ),
    )

    def __init__(self, boardnames=None, *args, **kwargs):
        super(TimeConfigFrm, self).__init__(*args, **kwargs)
        if boardnames:
            self.fields['no_of_boards'].choices = boardnames
