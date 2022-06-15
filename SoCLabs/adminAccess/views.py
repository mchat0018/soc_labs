from django.forms import formset_factory
from django.shortcuts import redirect, render
from .forms import TimeConfigFrm
from slots.models import TimeConfig, Board
from datetime import datetime

# Create your views here.
def timeDiff(sh,sm,eh,em):
    if sm>em:
        eh -= 1
        em += 60
    return (eh-sh)*60+(em-sm)


def index(request,pk):
    boardnames = Board.objects.values_list('board_name', flat=True)
    boardnames = list(sorted(set(boardnames)))
    boardnames = [(str(i),str(i)) for i in boardnames]
    form = formset_factory(TimeConfigFrm, extra=int(pk))
    formset = form(form_kwargs={'boardnames': boardnames})
    if request.method == "POST":
        formset = form(request.POST)
        if formset.is_valid():
            for data in formset:
                day = data.cleaned_data.get('day')
                start_time_hours = data.cleaned_data.get('start_time_hours')
                start_time_minutes = data.cleaned_data.get('start_time_minutes')
                end_time_hours = data.cleaned_data.get('end_time_hours')
                end_time_minutes = data.cleaned_data.get('end_time_minutes')
                duration = data.cleaned_data.get('duration') # timeDiff(start_time_hours,start_time_minutes,end_time_hours,end_time_minutes)
                no_of_boards = data.cleaned_data.get('no_of_boards')
                TimeConfig(day=day, start_time_hours=start_time_hours,
                           start_time_minutes=start_time_minutes, end_time_hours=end_time_hours, end_time_minutes=end_time_minutes, duration=duration, no_of_boards=no_of_boards).save()
            return redirect(index,pk=pk)
    return render(request, "adminAccess/timeConfig.html", {'formset':formset})

def timeConfigFunc(request):
    boardsNames = Board.objects.values_list('board_name', flat=True)
    return render(request, "adminAccess/newTConfig.html", {'boardsNames':sorted(set(boardsNames)), 'TodayDay':datetime.today().strftime('%A')})