import email
from http.client import CONTINUE
import socket, cv2, pickle, struct
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
import cv2
import threading
from slots.models import *
from django.views.decorators import gzip
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
import pytz

import socket, cv2, pickle, struct
# host_ip = '192.168.53.132'
host_ip = '192.168.50.233'
port = 9999

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def camera_response(ip_addr):
    host_ip = ip_addr 
    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host_ip, port))
    data = b""
    payload_size = struct.calcsize("Q")
    # global data
    while True:          
            while len(data) < payload_size:
                packet = client_socket.recv(720)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
        
            while len(data) < msg_size:
                data += client_socket.recv(720)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            frame = cv2.flip(frame, 1)
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@login_required       
@gzip.gzip_page
def index(request,board_no,ip_addr):
    # running authentication of user in current time slot
    # getting current day and time
    ist = pytz.timezone('Asia/Kolkata')
    datetime_now = datetime.now(ist)
    curr_time = datetime_now.strftime('%H:%M')
    curr_time_hours,curr_time_minutes = tuple(curr_time.split(':'))
    curr_day = datetime.today().weekday()
    
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gte=curr_time_minutes)))

    timeslot = TimeSlot.objects.filter(crit).first()    #current time slot
    print(timeslot)
    day = DAYS_OF_WEEK[curr_day]
    
    booked_slot = Board.objects.filter(day=day).filter(time_slot=timeslot).filter(board_no=int(board_no)).first()
    print(booked_slot.board_user.username)
    
    if booked_slot.board_user.email == request.user.email and booked_slot.board_user.username == request.user.username:
        data= {
            'u_name': booked_slot.board_user.username,
            'IP' : ip_addr,
            'Port' : 56545
        }
        return render(request,'webcam/index.html',data)
    
    else:
        raise PermissionDenied
    
def fpgaview(request,ip_addr):
        try:
            return StreamingHttpResponse(camera_response(ip_addr), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            pass

        
