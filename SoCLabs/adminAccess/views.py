from asyncio.windows_events import NULL
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q
from courses.models import Course,Lab
from slots.models import IPAddress,Board,TimeConfig,TimeSchedule,TimeSlot
from .forms import *


def crud(request):
    coursenames = Course.objects.values_list('name', flat=True)
    coursenames = list(sorted(set(coursenames)))
    coursenames = [(str(i), str(i)) for i in coursenames]
    coursenames.insert(0, ('Select Course', 'Select Course'))
    form = ConfigsCRUD(coursenames=coursenames)

    if request.method == "POST":
        form = ConfigsCRUD(request.POST)
        if form.is_valid():
            form.save()
        return redirect("crud")

    configs = TimeConfig.objects.all()
    return render(request, "adminAccess/crud.html", {'form': form, "configs": configs})


def delete_config(request, pk):
    config = TimeConfig.objects.get(id=pk)
    config.delete()
    return redirect("crud")


def run_authentication(user,course):
    pass

@login_required
def admin_page(request,course_id):
    course = Course.objects.get(id=course_id)

    # running authentication for user
    # if logged-in user doesn't have staff credentials
    if not request.user.profile.staff_cred:
        raise PermissionDenied
    # if logged in user isn't a part of the course
    if request.user not in course.professors.all() and request.user not in course.staff.all():
        raise PermissionDenied
    
    # if form data was submitted
    if request.method=='POST':
        # getting the checked board objects from the submitted form
        checked_board_names = request.POST.getlist('board_name')
        print(checked_board_names)
        # if no boxes were checked
        if len(checked_board_names) == 0: messages.error(request,'Please select at least one board to be used')
        else:
            checked_boards = IPAddress.objects.filter(board_name__in=checked_board_names).all()
            print(checked_boards)
            # getting the board objects previously assigned to the course
            previous_boards = IPAddress.objects.filter(course=course).all()

            if previous_boards is not None and len(previous_boards) > 0:
                print(previous_boards)
                # setting the course field of the previously assigned boards to null
                for board in previous_boards: 
                    board.course = None
                    board.save()

            # setting the course attribute for the checked boards
            for board in checked_boards:
                board.course = course
                board.save()

            messages.success(request,'Boards selected...Slots created successfully')

            # return redirect('admin-page')


    # getting all available boards and the ones already included in the course
    available_boards = IPAddress.objects.filter(Q(course__isnull=True) | Q(course=course)).all()

    context = {
        'boards':available_boards,
        'course':course
    }

    return render(request,'adminAccess/config.html',context=context)
