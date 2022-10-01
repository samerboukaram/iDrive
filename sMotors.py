import IODMKS as iOD
import iServer
import iTime as iT


#Create Motor Server
Motors = iServer.Server('0.0.0.0',4000)

# #Initialize Odrive
# OD = iOD.ODESC()
# OD.Reboot()
# OD.DumpErrors()
# OD.EraseConfiguration()
# OD.PassSettings(0)
# OD.SetVelocityMode(0)

#initialize time to measure delay
t0, t1 =0, 0

while True:

    #check Delay, 
    if (t1-t0)*1000 > 100: #delay more than 100ms
        print("Delay")

    t0 = iT.t0()

    #Read RPM From Client
    print("listening")
    RPM = Motors.ReceiveMessage()
    # print('RPM',RPM)

    # #Set Speed
    # OD.SetSpeed(Axis = 0, RPM = 0) #RPM)

    t1 = iT.t0()
 