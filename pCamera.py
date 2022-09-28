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

ShowPreview = False
try:
    if sys.argv[2] == "Show": #get the Second argument to int
        ShowPreview = True
except:
    ShowPreview = False


2
#Create Publisher
Port = 2000 + CameraNumber
Publisher = iServer.Publisher('0.0.0.0',Port) #should be created before accessing camera, to kill the process if already in use

#Access Camera
Camera = iCAM.Camera(CameraNumber,320,240, Format = "MJPEG", FPS = 60)
print("Starting Stream For Camera Number ", CameraNumber, 'on Port:', Port)




while True:
    t0 = iT.t0()

    Frame = Camera.GetFrame()
    if Frame is not None:

        if ShowPreview:
            iCAM.DisplayFrame(Frame)


        # # Frame2 = iCAM.Canny(Frame)
        # Frame2 = iCAM.FinCountours(Frame)
        # iCAM.DisplayFrame(Frame2, "Canny")

        Publisher.PublishImage("CAMERA",Frame)

    # print("FPS", iT.GetFPS(t0))





