import cv2
import os
import iOS

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

#CHECK old functions to get camera prop form ubuntu


def GetAllCameraResolutions(CameraNumber):

    #Get all resolutions for a camera, compare with list of common resolutions from wikipedia

    import pandas as pd

    url = "https://en.wikipedia.org/wiki/List_of_common_resolutions"
    table = pd.read_html(url)[0]
    table.columns = table.columns.droplevel()
    cap = cv2.VideoCapture(5)
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


def StartCameraByNumber(CameraNumber, ShowPreview = False, CameraPublisherPath = iOS.GetThisPath() + "/pCamera.py "):
    
    if ShowPreview:
        FulllPath =  CameraPublisherPath + str(CameraNumber) + " " + "Show"
    else:
        FulllPath =  CameraPublisherPath + str(CameraNumber)

    iOS.StartProcess(FulllPath)
    # if ShowPreview:
    #     os.popen("nohup python3 " +  CameraPublisherPath + str(CameraNumber) + " " + "Show")
    # else:
    #     os.popen("nohup python3 " + CameraPublisherPath + str(CameraNumber))


def PrintCamerasInfo():
    for n in range(len(GetCamerasNumbersAndNames()[0])): #Camera Numbers
            CameraNumber = GetCamerasNumbersAndNames()[0][n]
            CameraName =GetCamerasNumbersAndNames()[1][n]
            print("Camera Number:", CameraNumber, "         -----       Name:", CameraName, "       -----     Default Resolution:", GetCameraDefaultResolution(CameraNumber))
        

    

def DisplayFrame(Frame, Title = None, FPS = None):
  
    if FPS: 
        Frame = FPSOnFrame(Frame.copy(),FPS) #Write on a copy not to overide the original one
       
    
    if Title:
        cv2.imshow(Title,Frame)
    else:
        cv2.imshow("Frame",Frame)
    Key = cv2.waitKey(1)
    
    if Key == 113:  #q key is pressed
        print("exiting")
        exit()


def SplitStereoFrame(Frame):  #horizontal stereo iamge
    Frame1 = Frame[:,0:int(Frame.shape[1]/2),:]
    Frame2 = Frame[:,int(Frame.shape[1]/2):,:]

    return Frame1, Frame2



#Old fucntions from computer vision
    
def Canny(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    return imgCanny


def FinCountours(img):
    originalimage = img

    contours, hierarchy = cv2.findContours(Canny(img), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    count = 0
    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 10:   #10
            cv2.drawContours(originalimage, cnt, -1, (255, 20, 50), 3)  #3
            # cv2.imshow("Contours", originalimage)
            # cv2.waitKey(0)
     
            count = count +1
            # print(area)
    print("number of contours", count)
    return originalimage




if __name__ == '__main__':
  pass