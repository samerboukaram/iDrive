import paramiko
import os



def RunLocalScriptOnServer(Script, Username, Server, Password = None):
    Command = "cat " + Script + "  | ssh " + Username + "@" + Server + " python3 -"
    # print(Command)
    os.system(Command)




class SSHConnection:
    
    def __init__(self, Host = '172.104.253.25', Username = 'root', Password = 'sboukaram__12'):

        #Connect
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(Host, username=Username, password=Password)

    def RunCommand(self, Command):
        #Run Command
        _stdin, _stdout,_stderr = self.client.exec_command(Command)  #dir #sudo dir
        # _stdin.write('sboukaram__12\n')  #uncomment with sudo
        print(_stdout.read().decode())

    def CloseConnection(self):
        self.client.close()





#########################################################


# #Uploading
# ftp_client=client.open_sftp()
# ftp_client.put('/home/interdrive/Documents/iDrive/iROS.py','/root/iROS.py')
# ftp_client.close()

# # Downloading
# ftp_client=client.open_sftp()
# ftp_client.get('/home/interdrive/Documents/iDrive/server/f.py','/root/CameraLoadImage.py')
# ftp_client.close()


#############################################################$


# import paramiko   
   
# # declare credentials   
# host = '172.104.253.25'
# username = 'root'
# password = 'sboukaram__12'  
   
# # connect to server   
# con = paramiko.SSHClient()   
# con.load_system_host_keys()   
# con.connect(host, username=username, password=password)   
   
# # run the command   
# # use the -1 argument so we can split the files by line   
# stdin, stdout, stderr = con.exec_command('ls -1 /tmp')   
   
# # process the output   
# if stderr.read() == b'':   
#     for line in stdout.readlines():   
#         print(line.strip()) # strip the trailing line breaks   
# else:   
#     print(stderr.read()) 


