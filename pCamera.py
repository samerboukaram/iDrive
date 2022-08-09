import iCamera as iCAM
import iServer
import sys


#Print Infomation
print(iCAM.GetCamerasNumbersAndNames())

#Get Camera Number it it was supplied by arguments
try:
    CameraNumber = int(sys.argv[1]) #get the first argument to int
    print("Camera Number received from argument", CameraNumber)
except:
    print("No Camera Number received in argument")
    # exit()



#Get Camera Number From Camera Name
CameraNumber = iCAM.GetCameraNumberByName('USB 2.0 Camera: USB Camera')
print("Starting Stream For Camera Number ", CameraNumber)

#Create Publisher
Port = 2000 + CameraNumber
Publisher = iServer.Publisher('0.0.0.0',Port) #should be created before accessing camera, to kill the process if already in use

#Access Camera
Camera = iCAM.Camera(CameraNumber,640,480) 
print("Starting Stream For Camera Number ", CameraNumber, 'on Port:', Port)



while True:

    Frame = Camera.GetFrame()
    print(type(Frame))
    iCAM.DisplayFrame(Frame)

    Publisher.PublishImage("CAMERA",Frame)





