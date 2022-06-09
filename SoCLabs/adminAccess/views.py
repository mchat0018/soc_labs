from django.forms import formset_factory
from django.shortcuts import redirect, render
from .forms import TimeConfigFrm
from slots.models import TimeConfig

# Create your views here.
def index(request,pk):
    form = formset_factory(TimeConfigFrm,extra=pk)
    formset = form()
    if request.method == "POST":
        formset = form(request.POST)
        if formset.is_valid():
            for data in formset:
                day = data.cleaned_data.get('day')
                start_time_hours = data.cleaned_data.get('start_time_hours')
                start_time_minutes = data.cleaned_data.get('start_time_minutes')
                end_time_hours = data.cleaned_data.get('end_time_hours')
                end_time_minutes = data.cleaned_data.get('end_time_minutes')
                duration = data.cleaned_data.get('duration')
                no_of_boards = data.cleaned_data.get('no_of_boards')
                if day:
                    TimeConfig(day=day, start_time_hours=start_time_hours,
                                start_time_minutes=start_time_minutes, end_time_hours=end_time_hours, end_time_minutes=end_time_minutes, duration=duration, no_of_boards=no_of_boards).save()
            return redirect("index")
    fields = TimeConfig.objects.all()
    return render(request, "adminAccess/timeConfig.html", {'formset':formset})