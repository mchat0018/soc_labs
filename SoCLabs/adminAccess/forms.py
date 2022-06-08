from django import forms
from slots.models import TimeConfig

days = [
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
]

slots = [
    ('1', '10:00-10:30'),
    ('2', '10:30-11:00'),
    ('3', '11:00-11:30'),
]

class TimeConfigFrm(forms.ModelForm):
    class Meta:
        model = TimeConfig
        fields = "__all__"

    day = forms.CharField(
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "placeholder": "Select Day...",
            },
            choices=days
        ),
    )

    timeSlot = forms.CharField(
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
            },
            choices=slots
        ),
    )
