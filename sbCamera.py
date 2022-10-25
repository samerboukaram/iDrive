import iServer
import iCamera as iCAM
import iTime as iT
import cv2

while True:
    t0 = iT.t0()
    image = iServer.SubscribeImage('192.168.0.121',2002,"CAMERA")
    # image = cv2.resize(image,(int(640),int(360)))
    # image2 = iServer.SubscribeImage('192.168.0.121',2001,"CAMERA")
    # image3 = iServer.SubscribeImage('192.168.0.121',2002,"CAMERA")
    # image = iServer.SubscribeImage('0.0.0.0',2002,"CAMERA")
    FPS = iT.GetFPS(t0)
    iCAM.DisplayFrame(image,"Server", FPS)
    print(FPS)
    # iCAM.DisplayFrame(image2,"Server2", FPS = iT.GetFPS(t0))
    # iCAM.DisplayFrame(image3,"Server3", FPS = iT.GetFPS(t0))


    