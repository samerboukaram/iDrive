import iCamera as iCAM
import iServer


#Print Infomation
print(iCAM.GetCamerasNumbersAndNames())


#Get Camera Number From Camera Name
CameraNumber = 0 #iCAM.GetCameraNumberByName('USB 2.0 Camera: USB Camera')
print("Starting Stream For Camera Number ", CameraNumber)

#Create Publisher
Port = 2000
Publisher = iServer.Publisher('0.0.0.0',Port) #should be created before accessing camera, to kill the process if already in use

#Access Camera
Camera = iCAM.Camera(CameraNumber) #,640,480) 
print("Starting Stream For Camera Number ", CameraNumber, 'on Port:', Port)



while True:

    Frame = Camera.GetFrame()
    # print(type(Frame))
    iCAM.DisplayFrame(Frame)

    Publisher.PublishImage("CAMERA",Frame)





