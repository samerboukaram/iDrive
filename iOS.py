#Ubuntu Test
import subprocess
import os
import signal

#Get This Path
import pathlib

def GetThisPath():
    ThisPath = str(pathlib.Path().resolve())
    return ThisPath


def KillProcessOnPort(PortNumber):

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


def GetAllPublishers():
    AllPublishers = []
    for file in os.listdir():
        if file.startswith('p') and file.endswith('.py'):
            AllPublishers.append(file)
    return AllPublishers

def GetAllPythonScripts():
    AllScripts = []
    for file in os.listdir():
        if file.endswith('.py'):
            AllScripts.append(file)
    return AllScripts

def GetAllServers():
    AllPublishers = []
    for file in os.listdir():
        if file.startswith('s') and file.endswith('.py'):
            AllPublishers.append(file)
    return AllPublishers

def GetAllClients():
    AllPublishers = []
    for file in os.listdir():
        if file.startswith('c') and file.endswith('.py'):
            AllPublishers.append(file)
    return AllPublishers

def GetAllDeployedApps():
    AllPublishers = []
    for file in os.listdir():
        if file.startswith('d') and file.endswith('.py'):
            AllPublishers.append(file)
    return AllPublishers


def CheckIfRunning(ScriptName): 

    
    AllProcesses = []

    ProcessLine = subprocess.check_output("ps -ef | grep " + ScriptName,shell=True).decode()
    ProcessLine = ProcessLine.split('\n') #split each line
    for Column in ProcessLine:
        Column = Column.split('   ') ##########split each column sometimes this is requiring three spaces, somtimes it is requiring 4
        try:
            ProcessID = Column[1]
            AllProcesses.append(ProcessID)
        except:
            pass

    Number = len(ProcessLine)  #3 not running, 4 or more is already running

    if Number == 3:
        return False, 0
       
    elif Number >3 :
        return True, AllProcesses

def SwitchProcess(ScriptName): #turn on if it was off, off if it was on
    
    Status, PIDList = CheckIfRunning(ScriptName)
    if not Status:
        StartProcess(ScriptName)
    else:
        EndProcessByList(PIDList)

def CheckIfRunningWithArgument(ScriptName, Argument): #can be merged with the previous function
    AllProcesses = []

    ProcessLine = subprocess.check_output("ps -ef | grep " + ScriptName,shell=True).decode()
    ProcessLine = ProcessLine.split('\n') #split each line
    for Column in ProcessLine:
        Column = Column.split('   ') ##########split each column sometimes this is requiring three spaces, somtimes it is requiring 4

        try:
            print(Column)
            print(Column[1])
            print(Column[3])

            if Column[3].split(' ')[2] == 'python3' and Column[3].split(' ')[3] == ScriptName and Column[3].split(' ')[4] == str(Argument):
                ProcessID = Column[1]
                AllProcesses.append(ProcessID)
        except:
            pass

    Number = len(AllProcesses) 

    if Number == 0:
        return False, 0
       
    elif Number >0 :
        return True, AllProcesses
    



def StartProcess(ScriptName):

    # os.popen("nohup python3 " + ScriptName)
    os.popen("screen python3 " + ScriptName)
    #SELECT BETWEEN nohup screen    os.popen os.system   subprocess.call
    # subprocess.call(["python3", "~/Documents/effective-adventure/" + ScriptName])
    # os.system("python3 ~/Documents/effective-adventure/" + ScriptName)
    # os.popen("screen python3 ~/Documents/effective-adventure/" + ScriptName)  #os.poopen
    # print(ScriptName + " Started")

    #     # os.system("nohup python3 " + ThisPath + "/pCamera.py " + CameraNumber)
    # # os.popen("screen python3 " + ThisPath + "/pCamera.py " + CameraNumber)  #os.poopen
    # # os.popen("nohup python3 " + ThisPath + "/pCamera.py " + CameraNumber + " " + "Show")  #os.poopen
    # os.popen("python3 " + ThisPath + "/pCamera.py " + CameraNumber + " " + "Show")  #os.poopen



def EndProcess(ProcessID):
    os.kill(int(ProcessID), signal.SIGKILL) 
    print(str(ProcessID) + " Killed")
    


def EndProcessByList(PIDList):
    for PID in PIDList:
        try:
            EndProcess(PID)
        except:
            pass



def CheckRequirements(ScriptFile):
    RequiredScripts = []

    #Requies ScriptName1 ScriptName2   ###this line must be added at start
    Line = open(ScriptFile).readline()

    if Line.startswith("#Requires"):
        Line = Line.strip().split(' ')  #strip removes the line break at the end

        for Pub in Line[1:]:  #skip the #Requires
            RequiredScripts.append(Pub)
    
    return RequiredScripts
        


