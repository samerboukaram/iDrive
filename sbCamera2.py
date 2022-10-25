import iServerOld as iServer
import iCamera as iCAM
import iTime as iT
import cv2

while True:
    t0 = iT.t0()
    client = iServer.CreateClientSocket('0.0.0.0',2002)
    image = iServer.ClientReadFrame(client)
    FPS = iT.GetFPS(t0)
    iCAM.DisplayFrame(image,"Server", FPS)
    print(FPS)
    # iCAM.DisplayFrame(image2,"Server2", FPS = iT.GetFPS(t0))
    # iCAM.DisplayFrame(image3,"Server3", FPS = iT.GetFPS(t0))


    