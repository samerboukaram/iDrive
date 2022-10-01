import iServer as iSV
import iTime as iT
import iBytes as iBy
import iCamera as iCAM


#Create Server
Server = iSV.Server('0.0.0.0','1500')

#Create Publisher
Publisher = iSV.Publisher('0.0.0.0',1510) 

FPS = 0

while True:
    t0 = iT.t0()

    FrameData = Server.ReceiveFrameDataFile()

    #Dispaly Frame
    Frame  = iBy.DecodeFrame(FrameData)
    iCAM.DisplayFrame(Frame,"SSH SERVER (Saving)", FPS)
 

    #Publish Image To network
    Publisher.PublishImage("CAMERA",Frame)

    # # #Save data to file
    # iBy.SaveData(FrameData,'FrameData')


    FPS = iT.GetFPS(t0)



