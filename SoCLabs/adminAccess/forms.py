from django import forms
from slots.models import TimeConfig

days = [
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
]

hrs = [
    ('1', '10'),
    ('2', '11'),
    ('3', '12'),
]

mins = [
    ('1', '00'),
    ('2', '15'),
    ('3', '30'),
    ('4', '45'),
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
            },
            choices=hrs
        ),
    )

    start_time_minutes = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
                "placeholder": "Select Day...",
            },
            choices=mins
        ),
    )

    end_time_hours = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
                "placeholder": "Select Day...",
            },
            choices=hrs
        ),
    )

    end_time_minutes = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-select",
                "placeholder": "Select Day...",
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

    no_of_boards = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )