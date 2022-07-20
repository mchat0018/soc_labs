# from http.client import CONTINUE
# import socket, cv2, pickle, struct
#
# import cv2
# # from slots.models import *
# from datetime import datetime
# import pytz
#
# import socket, cv2, pickle, struct
# # from multiprocessing.connection import wait
import subprocess
from time import sleep
import paramiko


def connection(ip_addr, Board_id):
    host = ip_addr
    username = 'ecesoclab@iiitd.edu.in'
    password = 'ecesoclab@123'

    p = subprocess.Popen("python C:\Mihir\Django\SoCLabs\SoCLabs\webcam\connect.py " + str(host) + " " + str(Board_id),
                         creationflags=subprocess.CREATE_NEW_CONSOLE)

    sleep(5)

    # connect to server
    con = paramiko.SSHClient()
    con.load_system_host_keys()
    con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    con.connect(host, username=username, password=password)

    sftp_client = con.open_sftp()
    remote_file = sftp_client.open("E:\\remote_lab2\\" + Board_id + ".txt")
    hw_port = '0000'
    try:
        for line in remote_file:
            hw_port = line
            print(hw_port)
            break

    finally:
        remote_file.close()

    return hw_port


print(connection("192.168.33.161", "210248685247"))
