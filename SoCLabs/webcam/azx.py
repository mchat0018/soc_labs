from multiprocessing.connection import wait
import subprocess
from time import sleep
import paramiko

host = '192.168.33.161'
username = 'ecesoclab@iiitd.edu.in'
password = 'ecesoclab@123'

p = subprocess.Popen("python connect.py " + str(host), creationflags=subprocess.CREATE_NEW_CONSOLE)

sleep(5)

# connect to server
con = paramiko.SSHClient()
con.load_system_host_keys()
con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
con.connect(host, username=username, password=password)

sftp_client = con.open_sftp()
remote_file = sftp_client.open('E:\\remote_lab2\\port.txt')
port = '0000'
try:
    for line in remote_file:
        port = line
        print(port)
        

finally:
    remote_file.close()