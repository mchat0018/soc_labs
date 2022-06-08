from django.shortcuts import redirect, render
from .forms import TimeConfigFrm
from slots.models import TimeConfig

# Create your views here.
def index(request):
    form = TimeConfigFrm()
    if request.method == "POST":
        form = TimeConfigFrm(request.POST)
        #return render(request, "testing.html", {"text": form})
        if form.is_valid():
            form.save()
            
        return redirect("index")

    tasks = TimeConfig.objects.all()
    return render(request, "index.html", {"task_form": form, "tasks": tasks})