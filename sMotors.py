import iODMBS as iOD
import iServer


Motors = iServer.Server('0.0.0.0',3000)
# MotorLeft = iOD.Controller()
# MotorRight = iOD.Controller()

while True:
    print("listening")
    RPM = Motors.ReceiveMessage()
    print('RPM',RPM)
    # MotorLeft.SetSpeed(RPM)
    # MotorRight.SetSpeed(RPM)
    