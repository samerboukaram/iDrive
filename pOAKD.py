import iDepthAI as iDAI
import cv2
import iServer as iSV


#Create Publishers
Publisher = iSV.Publisher('0.0.0.0',2022) #should be created before accessing camera, to kill the process if already in use

#Create PipeLine
OAKD = iDAI.OakPipelines(RGB=True,Disparity=True, NN =True)


#Initial Values
RGBTS, RGBFrame = 0, None
LeftTS, LeftFrame = 0, None
RightTS, RightFrame = 0, None
DisparityTS, DisparityFrame = 0, None
nnTS, X, Y, Percentage = 0, None, None, None


while True:


    #Get Outputs from camera
    RGBFrame, RGBTS = OAKD.GetFrame('RGB', RGBFrame, RGBTS)
    LeftFrame, LeftTS = OAKD.GetFrame('MonoLeft', LeftFrame, LeftTS) #These two lines, left and right must be placed, or the depth wont update
    RightFrame, RightTS = OAKD.GetFrame('MonoRight', RightFrame, RightTS)
    DisparityFrame, DisparityTS = OAKD.GetFrame('Disparity', DisparityFrame, DisparityTS)
    DisparityFrame2, DisparityTS2 = OAKD.GetFrame('Disparity2', DisparityFrame, DisparityTS)
    # X,Y, Percentage = OAKD.GetNN(X,Y, Percentage, nnTS)


    # Display Frames
    if RGBFrame is not None:
        cv2.imshow("RGB", RGBFrame)
        Publisher.PublishImage("RGB",RGBFrame)
    if LeftFrame is not None:
        cv2.imshow("LeftFrame", LeftFrame)
        Publisher.PublishImage("MonoLeft",LeftFrame)
    if RightFrame is not None:
        cv2.imshow("RightFrame", RightFrame)
        Publisher.PublishImage("MonoRight",RightFrame)
    if DisparityFrame is not None:
        cv2.imshow("Depth", DisparityFrame)
        Publisher.PublishImage("Depth",DisparityFrame)
    if DisparityFrame2 is not None:
        cv2.imshow("Depth2", DisparityFrame2)
        Publisher.PublishImage("Depth2",DisparityFrame2)
        




    if cv2.waitKey(1) == ord('q'):
        OAKD.Close()
        break


