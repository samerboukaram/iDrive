import iServer
import iCamera as iCAM


while True:
    image = iServer.SubscribeImage('0.0.0.0',2020,"CAMERA")
    iCAM.DisplayFrame(image)


# while True:
#     RGB = iServer.SubscribeImage('0.0.0.0',2022,"RGB")
#     iCAM.DisplayFrame(RGB)

#     # MonoLeft = iServer.SubscribeImage('0.0.0.0',2022,"MonoLeft")
#     # iCAM.DisplayFrame(MonoLeft)