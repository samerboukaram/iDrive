import iServer as iSV
import iTime as iT
import iBytes as iBy
import iCamera as iCAM


#Create Server
Server = iSV.Server('0.0.0.0','1501')

FPS = 0

while True:
    t0 = iT.t0()
    
    # Request = Server.ReceiveMessage() #request for frame

    #Load Latest Frame
    FrameData = iBy.LoadData('FrameData')


    #Dispaly Frame
    try:
        Frame  = iBy.DecodeFrame(FrameData)
        iCAM.DisplayFrame(Frame,"SSH SERVER (Loading)", FPS)
    except:
        print('error')

    # #Send Data
    # Server.SendDataFile(FrameData)


    FPS = iT.GetFPS(t0)



