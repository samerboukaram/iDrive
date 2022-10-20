#Publish images and read them from the same server
import iTime as iT
import iBytes as iBY
import iServer as iSV
import iOS
import iCamera as iCAM

#Server Address
User = 'root'
# Address = '0.0.0.0'
Address = '172.104.253.25'
Port = '1510'


FPS = 0

while True:
    t0 = iT.t0()

    Image = iSV.SubscribeImage(Address,Port,"CAMERA")


    #DISPLAY FRAME
    
    iCAM.DisplayFrame(Image, "SSH Downloader", FPS)
  
   

    FPS = iT.GetFPS(t0)





# #Publish images and read them from the same server
# import iTime as iT
# import iBytes as iBY
# import iServer as iSV
# import iOS
# import iCamera as iCAM

# #Server Address
# User = 'root'
# Address = '0.0.0.0' #'172.104.253.25'
# Port = 1510


# # #Start Camera Server
# # SSH = iSSH.SSHConnection()
# # SSH.RunCommand("ls -1")
# # iOS.RunLocalScriptOnServer('SSHsLoadImage.py', User, '172.104.253.25')
# iOS.StartProcess('SSHsLoadImage.py')

# FPS = 0

# while True:
#     t0 = iT.t0()

#     #Create Client And Send Data
#     Client = iSV.Client(Address, Port)
#     # Client.SendFrame(Frame)
#     #SEND REQUEST
#     #GET FRAME
#     Frame = None

#     #DISPLAY FRAME
    
#     # iCAM.DisplayFrame(Frame, "SSH Uploader", FPS)
  
#     # print('sent')

#     FPS = iT.GetFPS(t0)

    


    


    

    



    
    





    