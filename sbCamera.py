import iServer
import iCamera as iCAM


while True:
    image = iServer.SubscribeImage('192.168.0.114',2009,"CAMERA")
    iCAM.DisplayFrame(image)

