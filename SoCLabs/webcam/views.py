from http.client import CONTINUE
import socket, cv2, pickle, struct
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
import cv2
from slots.models import *
from django.views.decorators import gzip
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
import pytz

import socket, cv2, pickle, struct
from multiprocessing.connection import wait
import subprocess
from time import sleep
import paramiko
# host_ip = '192.168.53.132'
# host_ip = '192.168.50.233'
# port = 9999

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
print("Hello")

def restart(ip_addr):
    
    # connect to server
    try:
        host = ip_addr
        username = 'ecesoclab@iiitd.edu.in'
        password = 'ecesoclab@123'
        con = paramiko.SSHClient()
        con.load_system_host_keys()
        con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        con.connect(host, username=username, password=password)
        print(host)


        # execute the script
        stdin, stdout, stderr = con.exec_command('python E:\\remote_lab2\\arduino.py')

        # printing the output of command
        print(stderr.read())
        output = (str(stdout.read()))

        print(output)

        if stderr.read() == b'':
            print('Success')
        else:
            print('An error occurred')

        # stdin, stdout, stderr = con.exec_command(r'E:\\Xilinx\\Vivado\\
        # 2019.1\\bin\\hw_server.bat -s TCP::' + port)


        # printing the output of command
        print(stderr.read())
        print(str(stdout.read()))

        if stderr.read() == b'':
            print('Success')
        else:
            print('An error occurred')
    except Exception as e:
        print(e)
        sleep(6)

def camera_response(ip_addr, cam_port, end_time):
    
    end_time = int(end_time)
    ist = pytz.timezone('Asia/Kolkata')
    datetime_now = datetime.now(ist)
    curr_time = datetime_now.strftime('%H:%M')
    curr_time_hours,curr_time_minutes = tuple(curr_time.split(':'))
    c_time = int(curr_time_hours+curr_time_minutes)
    
    host_ip = ip_addr 
    print(host_ip)
    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host_ip, int(cam_port)))
    data = b""
    payload_size = struct.calcsize("Q")
    # global data
    while c_time<end_time:          
            while len(data) < payload_size:
                packet = client_socket.recv(720)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            datetime_now = datetime.now(ist)
            curr_time = datetime_now.strftime('%H:%M')
            curr_time_hours,curr_time_minutes = tuple(curr_time.split(':'))
            c_time = int(curr_time_hours+curr_time_minutes)
        
            while len(data) < msg_size:
                data += client_socket.recv(720)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            frame = cv2.flip(frame, 1)
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def connection(ip_addr, Board_id):
    host = ip_addr
    username = 'ecesoclab@iiitd.edu.in'
    password = 'ecesoclab@123'

    p = subprocess.Popen(f"python .\connect.py {str(host)} {str(Board_id)}",
                         creationflags=subprocess.CREATE_NEW_CONSOLE)

    sleep(5)

    # connect to server
    con = paramiko.SSHClient()
    con.load_system_host_keys()
    con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    con.connect(host, username=username, password=password)

    sftp_client = con.open_sftp()
    remote_file = sftp_client.open(f"E:\\remote_lab2\\{Board_id}.txt")
    hw_port = '0000'
    try:
        for line in remote_file:
            hw_port = line
            print(hw_port)
            break

    finally:
        remote_file.close()

    return hw_port

@login_required       
@gzip.gzip_page
def index(request,course_id,board_serial):
    
    course = Course.objects.get(pk=course_id)
    # running authentication for logged in user
    if not request.user.profile.staff_cred:
        if request.user not in course.students.all():
            raise PermissionDenied
    else:
        if request.user not in course.professors.all() and request.user not in course.staff.all():
            raise PermissionDenied

    # running authentication of user in current time slot
    # getting current day and time
    ist = pytz.timezone('Asia/Kolkata')
    datetime_now = datetime.now(ist)
    curr_time = datetime_now.strftime('%H:%M')
    curr_time_hours,curr_time_minutes = tuple(curr_time.split(':'))
    curr_day = datetime.today().weekday()
    
    # getting the all the current and pending time slots for the day
    # criterion for getting time slots
    time_configs = TimeConfig.objects.filter(course=course).filter(day=DAYS_OF_WEEK[curr_day]).all()
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    
    timeslots = TimeSlot.objects.filter(crit).filter(time_config__in=time_configs).all()
    timeslots = list(timeslots)

    # if there are no time slots for the day left, permission denied
    if len(timeslots) == 0: raise PermissionDenied
    
    # sorting the time slots in increasing order
    timeslots.sort(key=lambda x: x.start_time_hours+x.start_time_minutes, reverse=False)
    # getting the closest time slot available
    timeslot = timeslots[0]    
    
    curr = curr_time_hours + curr_time_minutes
    st = timeslot.start_time_hours + timeslot.start_time_minutes
    # if closest time slot is not current time slot
    if curr < st: raise PermissionDenied
    
    print(curr_time)
    # print(timeslots)
    # print(type(timeslots))
    print(timeslot)

    day = DAYS_OF_WEEK[curr_day]
    
    # getting the board corresponding to the serial number
    ip_addr = IPAddress.objects.get(board_serial=board_serial)
    if ip_addr is None: raise PermissionDenied

    booked_slot = Board.objects.filter(course=course).filter(day=day).filter(time_slot=timeslot).filter(ip_addr=ip_addr).first()
    
    if booked_slot is not None and booked_slot.board_user is not None and booked_slot.board_user.username == request.user.username:
        hw_port = connection(ip_addr.ip, board_serial)
        end_time = booked_slot.time_slot.end_time_hours+booked_slot.time_slot.end_time_minutes

        # if request.POST:
        #     restart(ip_addr)
            
        data= {
            'u_name': booked_slot.board_user.username,
            'IP' : ip_addr,
            'board_serial': board_serial,
            'Port' : hw_port,
            'end_time':end_time,
            'course': course
        }
        return render(request,'webcam/index.html',data)
    
    else:
        raise PermissionDenied
    
def fpgaview(request,course_id,ip_addr,end_time,cam_port):
        try:
            return StreamingHttpResponse(camera_response(ip_addr,cam_port,end_time), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            pass
        
def restartView(request,course_id,board_serial):
    
    course = Course.objects.get(pk=course_id)
    # running authentication
    if not request.user.profile.staff_cred:
        if request.user not in course.students.all():
            raise PermissionDenied
    else:
        if request.user not in course.professors.all() and request.user not in course.staff.all():
            raise PermissionDenied

    # running authentication of user in current time slot
    # getting current day and time
    ist = pytz.timezone('Asia/Kolkata')
    datetime_now = datetime.now(ist)
    curr_time = datetime_now.strftime('%H:%M')
    curr_time_hours,curr_time_minutes = tuple(curr_time.split(':'))
    curr_day = datetime.today().weekday()
    
    # criterion for getting time slots
    time_configs = TimeConfig.objects.filter(course=course).filter(day=DAYS_OF_WEEK[curr_day]).all()
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    
    timeslots = TimeSlot.objects.filter(crit).filter(time_config__in=time_configs).all()
    timeslots = list(timeslots)
    
    # checking if the time slots are actually available
    if len(timeslots) == 0: raise PermissionDenied
    
    # sorting the time slots in ascending order of time
    timeslots.sort(key=lambda x: x.start_time_hours+x.start_time_minutes, reverse=False)
    timeslot = timeslots[0]    #current time slot
    
    # checking whether the first time slot on the list is actually the current time slot
    curr = curr_time_hours + curr_time_minutes
    st = timeslot.start_time_hours + timeslot.start_time_minutes

    if curr < st: raise PermissionDenied
    
    # print(curr_time)
    # print(timeslots)
    # print(type(timeslots))
    # print(timeslot)
    day = DAYS_OF_WEEK[curr_day]
    
    # extracting the currently booked board
    ip_addr = IPAddress.objects.get(board_serial=board_serial)
    if ip_addr is None: raise PermissionDenied

    booked_slot = Board.objects.filter(course=course).filter(day=day).filter(time_slot=timeslot).filter(ip_addr=ip_addr).first()
    # checking if the board user is the currently logged in user
    if booked_slot is not None and booked_slot.board_user is not None and booked_slot.board_user.username == request.user.username:
        restart(ip_addr.ip)
        data = {
            'ip_addr':ip_addr.ip,
            'u_name': booked_slot.board_user.username
        }
        return render(request,'webcam/restart.html',context=data)
    
    else: raise PermissionDenied

        
