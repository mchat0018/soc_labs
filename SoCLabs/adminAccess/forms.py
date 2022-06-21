from pyexpat import model
from django import forms
from courses.models import Course,Lab
from slots.models import TimeConfig,TimeSchedule,TimeSlot,IPAddress

class BoardSelectForm(forms.ModelForm):

    class Meta:
        model = IPAddress
        fields = ['board_name']