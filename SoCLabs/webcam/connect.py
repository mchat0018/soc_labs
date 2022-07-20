from logging import exception
from time import sleep
import paramiko
import sys

# connect to server
try:
    host = str(sys.argv[1])
    board_id = str(sys.argv[2])

    username = 'ecesoclab@iiitd.edu.in'
    password = 'ecesoclab@123'
    con = paramiko.SSHClient()
    con.load_system_host_keys()
    con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    con.connect(host, username=username, password=password)
    print(host)


    # execute the script
    stdin, stdout, stderr = con.exec_command('python E:\\remote_lab2\\execScript.py' + ' ' + board_id)
    print('abc')
    # printing the output of command
    print(stderr.read())
    output = (str(stdout.read()))
    port_start_idx = output.find("thePortIs") + 9
    port = output[port_start_idx:port_start_idx+5]
    print(port)

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
    sleep(60)