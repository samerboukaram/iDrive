import iCamera as iCAM
import iServer
import sys
import iTime as iT

#Get CameraNumber From Arguments
try:
    CameraNumber = int(sys.argv[1]) #get the first argument to int
except:
    print("Error: supply camera number in argument")
    exit()

#Get Preview Status From Arguments
ShowPreview = False
try:
    if sys.argv[2] == "Show": #get the Second argument to int
        ShowPreview = True
except:
    ShowPreview = False


#Create Publisher
Port = 2000 + CameraNumber
Publisher = iServer.Publisher('0.0.0.0',Port) #should be created before accessing camera, to kill the process if already in use

#Access Camera
Camera = iCAM.Camera(CameraNumber,640*2, 360*2, Format = "MJPEG", FPS = 50)
print("Starting Stream For Camera Number ", CameraNumber, 'on Port:', Port)


FPS = 0

while True:
    try:
        t0 = iT.t0()

        Frame = Camera.GetFrame()
        if Frame is not None:

            if ShowPreview:
                iCAM.DisplayFrame(Frame, "Camera Publisher", FPS)

            Publisher.PublishImage("CAMERA",Frame)

        FPS = iT.GetFPS(t0)
    except:
        Camera.Close()





