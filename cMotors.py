import iServer
import iPS4

PS4 = iPS4.PS4Controller()

i=1
while True:

    #Read PS4 Values
    PS4.GetValues()

    #Create Client
    Client = iServer.Client('192.168.43.86',3000)
    Client.Send(PS4.LeftStickUD)
