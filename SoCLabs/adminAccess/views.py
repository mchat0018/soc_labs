from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q
from courses.models import Course,Lab
from slots.models import IPAddress,Board,TimeConfig,TimeSchedule,TimeSlot

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
        # if no boxes were checked
        if len(checked_board_names) == 0: messages.error('Please select at least one board to be used')
        else:
            checked_boards = IPAddress.objects.filter(board_name__in=checked_board_names).all()
            # getting the board objects previously assigned to the course
            previous_boards = IPAddress.objects.filter(course=course).all()

            # deleting all the slots associated with the previouly assigned boards
            Board.objects.filter(ip_addr__in=previous_boards).delete()

            # creating fresh slots from the TimeConfigs defined for the course
            time_configs = TimeConfig.objects.filter(course=course).all()

            for time_config in time_configs.all():
                time_scheds = TimeSchedule.objects.filter(time_config=time_config).all()
                for time_sched in time_scheds.all():
                    for board in checked_boards:
                        Board.objects.create(day=time_sched.day,time_slot=time_config.time_slot,
                                        board_name=board.board_name,ip_addr=board,course=course)
            
            messages.success('Boards selected...Slots created successfully')

            # return redirect('admin-page')


    # getting all available boards and the ones already included in the course
    available_boards = IPAddress.objects.filter(Q(course__isnull=True) | Q(course=course)).all()

    context = {
        'boards':available_boards,
        'course':course
    }

    return render(request,'adminAccess/config.html',context=context)