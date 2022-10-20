#Requires pWebCam.py

import iServer as iSV
import iCamera as iCAM
import iMediaPipe as iMP2
import iTime as iT
import iStereoDepth as iST


#Pose Object
Pose = iMP2.MediaPipePose()



Frame = 0
while True:
    try:
        t0 = iT.t0()
        # print("Frame", Frame)

        #Subscribe to webcam
        Image = iSV.SubscribeImage('0.0.0.0','2000',"CAMERA")
        Image, Right = iST.SplitStereoImage(Image)
        Image = iCAM.cv2.resize(Image,(int(640/2),int(480/2)))

        
        #DetectPose
        Results= Pose.DetectPose(Image)

        # if Frame > 1:
        Pose.DrawPoseOnImage(Image,Results)
        Pose.GetLandMarks(0)  #nose Position
        DeltaX = Pose.GetCenterOfGravity()  #center of gravity
        Distance = Pose.GetShouldersDistance()  #Shoulder Distance

       
        FPS = iT.GetFPS(t0) 
        
        iCAM.DisplayFrame(Pose.Image,FPS = FPS)

        
        Frame = Frame+1
    except:
        print("Error")
