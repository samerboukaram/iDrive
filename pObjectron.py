#Requires pWebCam.py

import iServer
import iCamera as iCAM
import iMediaPipe as iMP
import time



#Pose Object
Pose = iMP.MediapipeObjectron()

#Publish Results
Pub = iServer.Publisher('0.0.0.0','2021')


Frame = 0
while True:
    # try:
        t0 = time.time()
        # print("Frame", Frame)

        #Subscribe to webcam
        Image = iServer.SubscribeImage('0.0.0.0',2000,"CAMERA")
        # Image = iServer.SubscribeImage('0.0.0.0',2022,"RGB")
        # Image = iCAM.cv2.resize(Image,(int(640/2),int(480/2)))

        
        #DetectPose
        Results= Pose.DetectObjectron(Image)

        # if Frame > 1:
        Pose.DrawObjectronOnImage(Image,Results)
     

        #Publish Results
        # Pub.PublishString("DeltaX",str(DeltaX))
        # Pub.PublishString("Distance",str(Distance))


        iCAM.DisplayFrame(Pose.Image)


        tend = time.time()
        FPS = 1/(tend-t0) 
        print("FPS", FPS)
        Frame = Frame+1
    # except:
    #     print("Error")
