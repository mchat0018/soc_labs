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
port = 9999

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

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

def camera_response(ip_addr,end_time):
    
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

    client_socket.connect((host_ip, port))
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

def connection(ip_addr):
    host = ip_addr
    username = 'ecesoclab@iiitd.edu.in'
    password = 'ecesoclab@123'

    p = subprocess.Popen("python D:\\Django\\SoCLabs\\SoCLabs\\webcam\\connect.py " + str(host) , creationflags=subprocess.CREATE_NEW_CONSOLE)

    sleep(5)

    # connect to server
    con = paramiko.SSHClient()
    con.load_system_host_keys()
    con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    con.connect(host, username=username, password=password)

    sftp_client = con.open_sftp()
    remote_file = sftp_client.open('E:\\remote_lab2\\port.txt')
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
def index(request,course_id,board_name,ip_addr):
    
    course = Course.objects.filter(pk=course_id)
    # running authentication
    if not request.user.staff_cred:
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
    
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    timeslots = TimeSlot.objects.filter(crit).all()
    timeslots = list(timeslots)
    if len(timeslots) == 0: raise PermissionDenied
    
    timeslots.sort(key=lambda x: x.start_time_hours+x.start_time_minutes, reverse=False)
    timeslot = timeslots[0]    #current time slot
    
    curr = curr_time_hours + curr_time_minutes
    st = timeslot.start_time_hours + timeslot.start_time_minutes
    # en = timeslot.end_time_hours + timeslot.end_time_minutes
    if curr < st: raise PermissionDenied
    
    print(curr_time)
    # print(timeslots)
    # print(type(timeslots))
    print(timeslot)
    day = DAYS_OF_WEEK[curr_day]
    
    booked_slot = Board.objects.filter(course=course).filter(day=day).filter(time_slot=timeslot).filter(board_name=board_name).first()
    
    if booked_slot.board_user is not None and booked_slot.board_user.username == request.user.username and ip_addr == booked_slot.ip_addr.ip:
        hw_port = connection(ip_addr)
        end_time = booked_slot.time_slot.end_time_hours+booked_slot.time_slot.end_time_minutes
        
        # if request.POST:
        #     restart(ip_addr)
            
        data= {
            'u_name': booked_slot.board_user.username,
            'IP' : ip_addr,
            'board_name': board_name,
            'Port' : hw_port,
            'end_time':end_time
        }
        return render(request,'webcam/index.html',data)
    
    else:
        raise PermissionDenied
    
def fpgaview(request,ip_addr,end_time):
        try:
            return StreamingHttpResponse(camera_response(ip_addr,end_time), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            pass
        
def restartView(request,course_id,board_name,ip_addr):
    
    course = Course.objects.filter(pk=course_id)
    # running authentication
    if not request.user.staff_cred:
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
    
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    timeslots = TimeSlot.objects.filter(crit).all()
    timeslots = list(timeslots)
    # checking if the time slots are actually available
    if len(timeslots) == 0: raise PermissionDenied
    
    timeslots.sort(key=lambda x: x.start_time_hours+x.start_time_minutes, reverse=False)
    timeslot = timeslots[0]    #current time slot
    
    # checking whether the first time slot on the list is actually the current time slot
    curr = curr_time_hours + curr_time_minutes
    st = timeslot.start_time_hours + timeslot.start_time_minutes
    # en = timeslot.end_time_hours + timeslot.end_time_minutes
    if curr < st: raise PermissionDenied
    
    # print(curr_time)
    # print(timeslots)
    # print(type(timeslots))
    # print(timeslot)
    day = DAYS_OF_WEEK[curr_day]
    # extracting the currently booked board
    booked_slot = Board.objects.filter(course=course).filter(day=day).filter(time_slot=timeslot).filter(board_no=board_name).first()
    # checking if the board user is the currently logged in user
    if booked_slot.board_user is not None and booked_slot.board_user.username == request.user.username and ip_addr == booked_slot.ip_addr.ip:
        restart(ip_addr)
        data = {
            'ip_addr':ip_addr,
            'board_name':board_name,
            'u_name': booked_slot.board_user.username
        }
        return render(request,'webcam/restart.html',context=data)
    
    else: raise PermissionDenied

        
