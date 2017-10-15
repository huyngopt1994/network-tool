import sys
import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/justin/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print ssh_session.rev(1024) # the the command from SSH server
        try:
            cmd_output = subprocess.check_output(command, shell=True)
            ssh_session.send(cmd_output)
        except Exception as e :
            ssh_session.send(str(e))
    return

if __name__ == '__main__':
    host_ip = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    command = sys.argv[4]
    ssh_command(host_ip, user, password, command)

