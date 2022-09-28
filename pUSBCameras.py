import os
import iCamera as iCAM

#Get This Path
import pathlib
ThisPath = str(pathlib.Path().resolve())



#Print Infomation
for n in range(len(iCAM.GetCamerasNumbersAndNames()[0])): #Camera Numbers
        CameraNumber = iCAM.GetCamerasNumbersAndNames()[0][n]
        CameraName =iCAM.GetCamerasNumbersAndNames()[1][n]
        print("Camera Number:", CameraNumber, "         -----       Name:", CameraName, "       -----     Default Resolution:", iCAM.GetCameraDefaultResolution(CameraNumber))
    


for CameraNumber in iCAM.GetCamerasNumbersAndNames()[0]:
        print("starting", CameraNumber)
        # os.system("nohup python3 " + ThisPath + "/pCamera.py " + CameraNumber)
        # os.popen("screen python3 " + ThisPath + "/pCamera.py " + CameraNumber)  #os.poopen
        # os.popen("nohup python3 " + ThisPath + "/pCamera.py " + CameraNumber + " " + "Show")  #os.poopen
        os.popen("python3 " + ThisPath + "/pCamera.py " + CameraNumber + " " + "Show")  #os.poopen