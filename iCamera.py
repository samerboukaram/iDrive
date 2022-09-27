import cv2
import os


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


#CHECK old functions to get camera prop form ubuntu




class Camera:

    def __init__(self, Number, Width = None, Height = None, Format = None, FPS = None):
        self.Capture = cv2.VideoCapture(Number)  # capture video from webcam 0
        if FPS: self.Capture.set(cv2.CAP_PROP_FPS, FPS)
        if Format == "MJPEG":self.Capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
        if Width: self.Capture.set(cv2.CAP_PROP_FRAME_WIDTH, Width)
        if Height: self.Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, Height)
       

    def GetFrameSize(self):
        Width  = int(self.Capture.get(cv2.CAP_PROP_FRAME_WIDTH))   
        Height = int(self.Capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        FPS = int(self.Capture.get(cv2.CAP_PROP_FPS))
        return str(Width)  + "x"+ str(Height) +" at " + str(FPS) + " FPS"

    #must be called to update the camera frame
    def GetFrame(self):
        suc,Frame = self.Capture.read()
        self.Frame = Frame
        return self.Frame

    def Close(self):
        # The following frees up resources and closes all windows
        self.Capture.release()
        cv2.destroyAllWindows()




def DisplayFrame(Frame):
    cv2.imshow("Frame",Frame)
    Key = cv2.waitKey(1)
    
    if Key == 113:  #q key is pressed
        print("exiting")
        exit()






if __name__ == '__main__':
  pass