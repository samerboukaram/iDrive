import os
import time
import signal

def KillProcessOnPort(Port):
    try:
        KillProcessLoop(int(Port))
        time.sleep(0.01)
    except:
        pass


    try:
        KillProcessLoop(int(Port))
        time.sleep(0.01)
    except:
        pass




def KillProcessLoop(PortNumber):

    output_command = os.popen("netstat -lntp").readlines()

    for line in output_command[2:]:
        Address = line[20:40].split(':')[0]
        try:
            Port = int(line[20:40].split(':')[1].split(' ')[0])
        except:
            Port = "None"
 
        PID = line[80:100].split('/')[0]

        if PortNumber == Port:
            EndProcess(PID)
            print("Process", PID, "Stopped on:", Address,Port)





def EndProcess(ProcessID):
    os.kill(int(ProcessID), signal.SIGKILL) 
    print(str(ProcessID) + " Killed")
    
