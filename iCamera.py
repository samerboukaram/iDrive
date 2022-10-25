from xml.dom.minidom import Identified
from xmlrpc.client import Server
import cv2
import os
import iOS
import iServer as iSV
import iServerOld as iSVO


#######FUNCTIONS TO GET CAMERAS IN SYSTEM


def GetFirstLineFromFile(FilePath): #used to search for camera properties
    File = open(FilePath)
    FirstLine = File.read().split('\n')[0]
    File.close()
    return FirstLine


def GetCamerasNumbersAndNames():
    #Ubuntu 20.04 path
    V4LDIR = "/sys/class/video4linux"

    #initialize lists
    CameraNames = []
    CameraNumbers = []

    #Get Cameras
    for Video in os.listdir(V4LDIR):

        CameraName = GetFirstLineFromFile(V4LDIR+"/"+Video+"/name")
        CameraIndex = int(GetFirstLineFromFile(V4LDIR+"/"+Video+"/index"))
        CameraNumber = Video.split('video')[1] #get just the number
    
        if CameraIndex == 0:
            CameraNames.append(CameraName)
            CameraNumbers.append(CameraNumber)

    return CameraNumbers, CameraNames

def GetCameraNumberByName(CameraName):
    CameraNumbers, CameraNames = GetCamerasNumbersAndNames()

    for i in range(len(CameraNames)):
        if CameraNames[i]==CameraName:
            return int(CameraNumbers[i])


def GetCameraDefaultResolution(CameraNumber):
    Camera = cv2.VideoCapture(int(CameraNumber))
    Width = Camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    Height = Camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # print("Camera Number", CameraNumber, Width, Height)
    return Width, Height



def GetAllCameraResolutions(CameraNumber): #SOME RESOLUTIONS NOT FOUND FOR 9732 136deg camera!!!

    #Get all resolutions for a camera, compare with list of common resolutions from wikipedia

    import pandas as pd

    url = "https://en.wikipedia.org/wiki/List_of_common_resolutions"
    table = pd.read_html(url)[0]
    table.columns = table.columns.droplevel()
    cap = cv2.VideoCapture(CameraNumber)
    resolutions = {}
    for index, row in table[["W", "H"]].iterrows():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, row["W"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, row["H"])
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        resolutions[str(width)+"x"+str(height)] = "OK"
    print(resolutions)



def FPSOnFrame(Image, FPS):
    Image = cv2.putText(Image, str(FPS) + "FPS", (5,25), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(50,255,255),2,1)
    return Image


def GetCameraByNumberOrName(NumberOrName):
    if type(NumberOrName) == int : #check if int or str
        print("here")
        Number = NumberOrName
    elif type(NumberOrName) == str:
        Number = GetCameraNumberByName(NumberOrName)
    else:
        Number = None  
    return Number
    

class Camera:

    def __init__(self, CameraNumber, Width = None, Height = None, FPS = None, Publish = False):
       
        #Get Number
        self.Number = CameraNumber


        #Publisher
        if Publish:
            #Create Publisher
            self.Port = 2000 + self.Number
            #ZMQ
            self.Publisher = iSV.Publisher('0.0.0.0',self.Port) #created before accessing camera, to kill the process if already in use
            #SOCKET
            # self.Server = iSVO.CreateServerSocket('0.0.0.0', self.Port)

        #Get Camera
        iOS.KillCamera(self.Number) #kill the camera process if it was already running
        self.Capture = cv2.VideoCapture(self.Number)  # capture video from webcam 0
        if FPS: self.Capture.set(cv2.CAP_PROP_FPS, FPS)
        self.Capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
        if Width: self.Capture.set(cv2.CAP_PROP_FRAME_WIDTH, Width)
        if Height: self.Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, Height)
        

    #must be called to update the camera frame
    def GetFrame(self):
        Success,Frame = self.Capture.read()
        self.Frame = Frame
        if Success:
            return self.Frame
        else:
            return None



                      
    def Close(self):
        # The following frees up resources and closes all windows
        self.Capture.release()
        cv2.destroyAllWindows()



def PrintCamerasInfo():
    for n in range(len(GetCamerasNumbersAndNames()[0])): #Camera Numbers
            CameraNumber = GetCamerasNumbersAndNames()[0][n]
            CameraName =GetCamerasNumbersAndNames()[1][n]
            print("Camera Number:", CameraNumber, "         -----       Name:", CameraName, "       -----     Default Resolution:", GetCameraDefaultResolution(CameraNumber))
        

    

def DisplayFrame(Frame, Title = None, FPS = None):
  
    if FPS: 
        Frame = FPSOnFrame(Frame.copy(),FPS) #Write on a copy not to overide the original one
       
    if Title is None:
        Title = "Frame"

    cv2.imshow(Title,Frame)
    Key = cv2.waitKey(1)
    
    if Key == 113:  #q key is pressed
        cv2.destroyWindow(Title)
        exit()




def LaunchCamera(CameraNumber, Width, Height, FPS, ShowPreview, Publish):

    #get this python script name to launch the current scipt in a new process
    Script = os.path.basename(__file__) 

    #Launch script in new external thread with arguments
    os.popen("python3 " + Script + " " +str(CameraNumber)
                                 + " " +str(Width)
                                 + " " +str(Height)
                                 + " " +str(FPS)
                                 + " " +str(ShowPreview)
                                 + " " +str(Publish)
                                 )





#USED TO LAUNCH A CERTAIN CAMERA IN AN INDEPENDANT PROCESS
if __name__ == '__main__':

    import sys
    import iTime as iT
  

    try:
        #Get Arguments
        CameraNumber = int(sys.argv[1])
        Width = int(sys.argv[2])
        Height = int(sys.argv[3])
        FPS = int(sys.argv[4])
        ShowPreview = (str(sys.argv[5]) == "True")
        Publish = (str(sys.argv[6]) == "True")
    except:
        print("Camera Arguments Missing")
        exit()


    Cam = Camera(CameraNumber, 
            Width = Width, Height = Height, FPS = FPS,Publish= Publish)

    FPS = 0

    while True:
        # try:
            t0 = iT.t0()

            Frame = Cam.GetFrame()
            if Frame is not None:
                if ShowPreview:
                    DisplayFrame(Frame, "Camera Publisher", FPS)

                if Publish:
                    pass
                    #ZMQ
                    Cam.Publisher.PublishImage("CAMERA",Frame)
                    #Socket
                    # iSVO.ServerSendFrame(Cam.Server, Frame)
            FPS = iT.GetFPS(t0)
            print(FPS)
        # except:
        #     iOS.KillCamera(CameraNumber)
        #     # Cam.Close()
        #     exit() #to close the while loop
    





