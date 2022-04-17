from http.client import CONTINUE
import socket, cv2, pickle, struct
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import threading
from django.views.decorators import gzip

import socket, cv2, pickle, struct
# host_ip = '192.168.53.132'
host_ip = '192.168.0.49'
port = 9999


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
        
@gzip.gzip_page
def index(request):
    
    data= {
        'IP' : host_ip,
        'Port' : 56545
    }
    return render(request,'webcam/index.html',data)

def fpgaview(request,ip_addr):
        try:
            return StreamingHttpResponse(camera_response(ip_addr), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            pass

        
