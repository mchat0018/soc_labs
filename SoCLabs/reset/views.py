from django.shortcuts import render, redirect
from slots.models import Board

# Create your views here.
def reset(request):
    if request.method == "POST":
        boards = Board.objects.all()
        boards.update(board_user = None)
        return redirect("reset")
    return render(request,'reset/reset.html')