import IODMKS as iOD
import iServer


Motors = iServer.Server('0.0.0.0',3000)

#Initialize Odrive
OD = iOD.ODESC()
OD.Reboot()
OD.DumpErrors()
OD.EraseConfiguration()
OD.PassSettings(0)
OD.SetVelocityMode(0)


while True:

    #Read RPM From Client
    print("listening")
    RPM = Motors.ReceiveMessage()
    print('RPM',RPM)

    #Set Speed
    OD.SetSpeed(Axis = 0, RPM = 0) #RPM)

  