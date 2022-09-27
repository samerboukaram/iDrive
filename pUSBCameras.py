import os
import iCamera as iCAM


#Print Infomation
print(iCAM.GetCamerasNumbersAndNames()[0])

for CameraNumber in iCAM.GetCamerasNumbersAndNames()[0]:
        print("starting", CameraNumber)
        # os.system("nohup python3 ~/Documents/iDrive/pCamera.py " + CameraNumber)
        # os.popen("screen python3 ~/Documents/iDrive/pCamera.py " + CameraNumber)  #os.poopen
        # os.popen("nohup python3 ~/Documents/iDrive/pCamera.py " + CameraNumber)  #os.poopen
        os.popen("python3 ~/Documents/iDrive/pCamera.py " + CameraNumber)  #os.poopen