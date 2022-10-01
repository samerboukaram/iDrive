import os
import iCamera as iCAM
import iOS


ThisPath = iOS.GetThisPath()




#Print Infomation
iCAM.PrintCamerasInfo()


for CameraNumber in iCAM.GetCamerasNumbersAndNames()[0]:
        print("starting", CameraNumber)
        # os.system("nohup python3 " + ThisPath + "/pCamera.py " + CameraNumber)
        # os.popen("screen python3 " + ThisPath + "/pCamera.py " + CameraNumber)  #os.poopen
        os.popen("nohup python3 " + ThisPath + "/pCamera.py " + CameraNumber + " " + "Show")  #os.poopen
        # os.popen("python3 " + ThisPath + "/pCamera.py " + CameraNumber + " " + "Show")  #os.poopen