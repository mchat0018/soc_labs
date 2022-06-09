from django.shortcuts import redirect, render
from .forms import TimeConfigFrm
from slots.models import TimeConfig

# Create your views here.
def index(request):
    form = TimeConfigFrm()
    if request.method == "POST":
        form = TimeConfigFrm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("index")

    fields = TimeConfig.objects.all()
    return render(request, "adminAccess/timeConfig.html", {"form": form, "fields": fields})
