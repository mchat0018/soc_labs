from asyncio.windows_events import NULL
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q
from courses.models import Course,Lab
from slots.models import IPAddress,Board,TimeConfig,TimeSchedule,TimeSlot,StartDay
from .forms import ConfigsCRUD

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def ret_lab_days(offset):
    day_list = []

    for i in range(7):
        day_list.append(DAYS_OF_WEEK[(i + offset) % 7])
    
    return day_list

# dictionary of days for key reference during sorting
def ret_day_dict(course):
    offset = StartDay.objects.filter(course=course).first().day
    lab_days = ret_lab_days(offset)
    day_dict = {}

    for i in range(len(lab_days)): day_dict[lab_days[i]] = i
    return day_dict

def run_authentication(user, course):
    # if logged-in user doesn't have staff credentials
    if not user.profile.staff_cred:
        return False
    # if logged in user isn't a part of the course
    if user not in course.professors.all() and user not in course.staff.all():
        return False

    return True

@login_required
def adminRts(request, course_id):
    course = Course.objects.get(id=course_id)

    # running authentication for user
    if not run_authentication(request.user, course):
        raise PermissionDenied


    # if form data was submitted
    if request.method == "POST":
        # getting the checked board objects from the submitted form
        checked_board_names = request.POST.getlist('board_name')
        print(checked_board_names)
        # if no boxes were checked
        if len(checked_board_names) == 0:
            messages.error(
                request, 'Please select at least one board to be used')
        else:
            checked_boards = IPAddress.objects.filter(
                board_name__in=checked_board_names).all()
            print(checked_boards)
            # getting the board objects previously assigned to the course
            previous_boards = IPAddress.objects.filter(course=course).all()

            # maintaining a list of boards which were kept as is, so as to avoid removing unnecessary
            # slots
            common_boards = []

            if previous_boards is not None and len(previous_boards) > 0:
                print(previous_boards)
                # setting the course field of the previously assigned boards to null
                for board in previous_boards:
                    # if the board has been actually removed
                    if board.board_name not in checked_board_names: 
                        board.course = None
                        board.save()
                    else: common_boards.append(board)

            # setting the course attribute for the checked boards
            for board in checked_boards:
                # to avoid duplicates
                if board not in common_boards:
                    board.course = course
                    board.save()

            messages.success(
                request, 'Boards selected...Slots created successfully')

        form = ConfigsCRUD(request.POST)
        if form.is_valid():
            # checking if the entered timings are clashing with the others

            # getting the parameters from the form
            day = form.cleaned_data['day']
            start_time = form.cleaned_data['start_time_hours'] + form.cleaned_data['start_time_minutes']
            end_time = form.cleaned_data['end_time_hours'] + form.cleaned_data['end_time_minutes']
            slot_limit = form.cleaned_data['slot_limit']

            # if ending time is numerically smaller than starting time
            if end_time <= start_time:
                # if ending time exceeds midnight, it should be invalid
                if end_time > "0000": 
                    messages.error(request,'Please choose time slots within the day')
                    return redirect("adminRts", course_id=course_id)
                # if end_time is at midnight
                else:
                    end_time = "2400"

            # getting the TimeConfigs of the course on the day in question
            time_configs = TimeConfig.objects.filter(
                course=course).filter(day=day).all()
            
            # iterating through the time configs and checking for clashes
            if time_configs is not None and len(time_configs) > 0:
                for config in time_configs.all():
                    st = config.start_time_hours + config.start_time_minutes
                    ed = config.end_time_hours + config.end_time_minutes

                    # if ed is at midnight
                    if ed == "0000": ed = "2400"

                    # if timings clash, form object won't be saved
                    if end_time <= ed and end_time > st:
                        print('Failure to create slots due to timings clash.')
                        messages.error(
                            request, 'Failure to create slots due to timings clash.')
                        return redirect("adminRts", course_id=course_id)
                    if start_time >= st and start_time < ed:
                        print('Failure to create slots due to timings clash.')
                        messages.error(
                            request, 'Failure to create slots due to timings clash.')
                        return redirect("adminRts", course_id=course_id)

                    # checking if entered slot limit matches with all slot limits set for that day
                    lim = config.slot_limit
                    if(slot_limit!=lim): return redirect("adminRts", course_id=course_id)

            # setting the course attribute of the object
            form.instance.course = course
            # saving the object, now that it has passed all the tests
            form.save()
            messages.success(request, f'Slots successfully created')

            return redirect("adminRts", course_id=course_id)

    # getting all available boards and the ones already included in the course
    available_boards = IPAddress.objects.filter(
        Q(course__isnull=True) | Q(course=course)).all()

    form = ConfigsCRUD()
    
    # getting all the current TimeConfig objects
    configs = list(TimeConfig.objects.filter(course=course).all())
    # sorting the objects in ascending order of days and starting time
    day_dict = ret_day_dict(course)
    configs.sort(key=lambda x: str(day_dict[x.day]+1) + x.start_time_hours + x.start_time_minutes,
                 reverse=False
                 )

    return render(request, "adminAccess/adminRts.html", {'form': form, "configs": configs, "course": course, "boards": available_boards})


@login_required
def delete_config(request, course_id, pk):
    course = Course.objects.get(id=course_id)
    
    # running authentication for user
    if not run_authentication(request.user,course): raise PermissionDenied

    # fetching and deleting the object
    config = TimeConfig.objects.get(id=pk)
    config.delete()
    return redirect("adminRts",course_id=course_id)


@login_required
def reset(request, course_id):
    if request.method == "POST":
        course = Course.objects.get(id=course_id)

        # running authentication for user
        if not run_authentication(request.user,course): raise PermissionDenied

        # getiing all the slots of the course
        boards = Board.objects.filter(course=course).all()
        # setting the board_user attribute to None
        boards.update(board_user = None)

        return redirect("adminRts", course_id=course_id)
        
    return render(request,"adminAccess/adminRts.html")


# Earlier views (outdated, but kept for archiving purposes)
@login_required
def crud(request,course_id):
    course = Course.objects.get(id=course_id)
    
    # running authentication for user
    if not run_authentication(request.user,course): raise PermissionDenied

    # coursenames = Course.objects.values_list('name', flat=True)
    # coursenames = list(sorted(set(coursenames)))
    # coursenames = [(str(i), str(i)) for i in coursenames]
    # coursenames.insert(0, ('Select Course', 'Select Course'))
    form = ConfigsCRUD()

    # if form data was submitted
    if request.method == "POST":
        form = ConfigsCRUD(request.POST)
        if form.is_valid():
            # checking if the entered timings are clashing with the others
            
            # getting the parameters from the form
            day = form.cleaned_data['day']
            start_time = form.cleaned_data['start_time_hours'] + form.cleaned_data['start_time_minutes']
            end_time = form.cleaned_data['end_time_hours'] + form.cleaned_data['end_time_minutes']
            
            # getting the TimeConfigs of the course on the day in question
            time_configs = TimeConfig.objects.filter(course=course).filter(day=day).all()
            print(time_configs)
            # iterating through the time configs and checking for clashes
            if time_configs is not None and len(time_configs) > 0:
                for config in time_configs.all():
                    st = config.start_time_hours + config.start_time_minutes
                    ed = config.end_time_hours + config.end_time_minutes

                    # if timings clash, form object won't be saved
                    if ed <= end_time and ed > start_time:
                        messages.error(request,'Faliure to create slots due to timings clash.')
                        return redirect("edit-time",course_id=course_id)
                    if st >= start_time and st < end_time:
                        messages.error(request,'Faliure to create slots due to timings clash.')
                        return redirect("edit-time",course_id=course_id)

            # setting the course attribute of the object
            form.instance.course = course
            
            form.save()
            messages.success(request,f'Slots successfully created')
            return redirect("edit-time",course_id=course_id)
    

    # getting all the current TimeConfig objects 
    configs = list(TimeConfig.objects.filter(course=course).all())
    
    # sorting the objects in ascending order of days and starting time
    day_dict = ret_day_dict(course)
    configs.sort(key=lambda x: str(day_dict[x.day]+1) + x.start_time_hours + x.start_time_minutes,
                         reverse=False
    )
    
    return render(request, "adminAccess/crud.html", {'form': form, "configs": configs, "course": course })

@login_required
def board_page(request,course_id):
    course = Course.objects.get(id=course_id)

    # running authentication for user
    if not run_authentication(request.user,course): raise PermissionDenied
    
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

            return redirect('edit-board',course_id=course_id)


    # getting all available boards and the ones already included in the course
    available_boards = IPAddress.objects.filter(Q(course__isnull=True) | Q(course=course)).all()

    context = {
        'boards':available_boards,
        'course':course
    }

    return render(request,'adminAccess/config.html',context=context)

    # 