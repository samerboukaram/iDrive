import iServer
import iCamera as iCAM


while True:
    image = iServer.SubscribeImage('192.168.43.86',2000,"CAMERA")
    iCAM.DisplayFrame(image)

