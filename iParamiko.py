import paramiko

class SSHSession():

    def __init__(self, HOST='172.104.253.25', Username='root',Password='sboukaram__12'):

        #Connect
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(HOST, username=Username, password=Password)


    def RunCommand(self, Command):

        _stdin, _stdout,_stderr = self.client.exec_command(Command)  #sudo dir
        # _stdin.write('sboukaram__12\n')  #uncomment with sudo to input a password
        # return _stdout.read().decode()

        print("SSH Terminal:")
        while True: #print outputs line by line
            line = _stdout.readline()
            if not line:
                break
            print(line, end="")

    def CloseSession(self):
        self.client.close()


Cloud = SSHSession()
# Response = Cloud.RunCommand("gst-launch-1.0 udpsrc port=2000 ! queue ! tcpserversink host=0.0.0.0 port=3000")
# Cloud.RunCommand("apache2 -version")
Response = Cloud.RunCommand("gst-launch-1.0 udpsrc port=2000 ! tcpserversink host=0.0.0.0 port=3000")
# Response = Cloud.RunCommand("reboot")

Cloud.CloseSession()







# #Uploading
# ftp_client=client.open_sftp()
# ftp_client.put('/home/interdrive/Documents/iDrive/iROS.py','/root/iROS.py')
# ftp_client.close()

# # Downloading
# ftp_client=client.open_sftp()
# ftp_client.get('/home/interdrive/Documents/iDrive/server/f.py','/root/CameraLoadImage.py')
# ftp_client.close()


