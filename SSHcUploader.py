# Upload images to SSH server
import iTime as iT
import iBytes as iBY
import iServer as iSV
import iSSH
import iCamera as iCAM
import iOS

#Server Address
User = 'root'
# Address = '0.0.0.0'
Address = '172.104.253.25'
Port = 1500


# #Start Camera Server
# SSH = iSSH.SSHConnection()
# SSH.RunCommand("ls -1")
# iOS.RunLocalScriptOnServer('SSHsSaveImage.py', User, '172.104.253.25')
# iOS.StartProcess('SSHsSaveImage.py')

CameraNumber = 0

FPS = 0

while True:
    t0 = iT.t0()

    #Get Frame
    # iCAM.StartCameraByNumber(CameraNumber, True) #TODO: check if already was started, get the numbers automatically
    Frame = iSV.SubscribeImage('0.0.0.0',str(2000+CameraNumber),"CAMERA")
    iCAM.DisplayFrame(Frame, "SSH Uploader", FPS)


    #Create Client And Send Data
    Client = iSV.Client(Address, Port)
    Client.SendFrame(Frame)

  
    # print('sent')

    FPS = iT.GetFPS(t0)

    


    


    

    



    
    





    