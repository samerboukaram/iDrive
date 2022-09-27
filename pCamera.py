import iCamera as iCAM
import iServer
import sys

#Get CameraNumber From Arguments
try:
    CameraNumber = int(sys.argv[1]) #get the first argument to int
except:
    print("Error: supply camera number in argument")
    exit()



#Create Publisher
Port = 2000 + CameraNumber
Publisher = iServer.Publisher('0.0.0.0',Port) #should be created before accessing camera, to kill the process if already in use

#Access Camera
Camera = iCAM.Camera(CameraNumber) #,640,480, Format = "MJPEG", FPS = 30)
print("Starting Stream For Camera Number ", CameraNumber, 'on Port:', Port)



while True:

    Frame = Camera.GetFrame()
    # print(type(Frame))
    # iCAM.DisplayFrame(Frame)

    Publisher.PublishImage("CAMERA",Frame)





