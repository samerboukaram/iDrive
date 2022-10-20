import iServer
import iCamera as iCAM
import iTime as iT

while True:
    t0 = iT.t0()
    # image = iServer.SubscribeImage('192.168.0.121',2001,"CAMERA")
    image = iServer.SubscribeImage('0.0.0.0',2002,"CAMERA")
    iCAM.DisplayFrame(image,"Server", FPS = iT.GetFPS(t0))
