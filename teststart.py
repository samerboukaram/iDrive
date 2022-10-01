import os      
      
#SELECT BETWEEN nohup screen    os.popen os.system   subprocess.call
# subprocess.call(["python3", "~/Documents/effective-adventure/" + ScriptName])
# os.system("python3 ~/Documents/effective-adventure/" + ScriptName)
os.popen("screen python3 ~/Documents/effective-adventure/" + ScriptName)  #os.poopen
# print(ScriptName + " Started")

# os.system("nohup python3 " + ThisPath + "/pCamera.py " + CameraNumber)
# os.popen("screen python3 " + ThisPath + "/pCamera.py " + CameraNumber)  #os.poopen
# os.popen("nohup python3 " + ThisPath + "/pCamera.py " + CameraNumber + " " + "Show")  #os.poopen
os.popen("python3 " + ThisPath + "/pCamera.py " + CameraNumber + " " + "Show")  #os.poopen