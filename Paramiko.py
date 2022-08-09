import paramiko

command = "dir"


host = '172.104.253.25'
username = 'root'
password = 'sboukaram__12'

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
_stdin, _stdout,_stderr = client.exec_command("dir")  #sudo dir
# _stdin.write('sboukaram__12\n')  #uncomment with sudo
print(_stdout.read().decode())


# #Uploading
# ftp_client=client.open_sftp()
# ftp_client.put('/home/interdrive/Documents/iDrive/iROS.py','/root/iROS.py')
# ftp_client.close()

# Downloading
ftp_client=client.open_sftp()
ftp_client.get('/home/interdrive/Documents/iDrive/server/f.py','/root/CameraLoadImage.py')
ftp_client.close()


# COMMANDS REQUIRING INPUT
# Sometimes you need to provide a password or extra input to run a command. This is what stdin is used for. Let’s run the same command above with sudo.

# stdin, stdout, stderr = ssh.exec_command(“sudo ls”)
# stdin.write(‘mypassword\n’)
# print stdout.readlines()


client.close()


