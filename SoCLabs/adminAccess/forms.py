from django import forms
from slots.models import TimeConfig

days = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
]

hrs = [
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
]

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