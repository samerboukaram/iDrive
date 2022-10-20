import os
import iOS

output_command = os.popen("lsof /dev/video" + str(4)).readlines()

for line in output_command[2:]:
    print(line)
    PID = int(line.split(' ')[1])
    print(PID)


    iOS.EndProcess(PID)
    print("Process", PID, "Stopped")