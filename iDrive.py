import os

#Use No Hang Up to run Scripts


#Start Camera
a= os.system("nohup python3 ~/Documents/iDrive/pCamera.py -0 &")
print(a)
#Stream Camera
os.system("nohup python3 ~/Documents/iDrive/pFlask.py &")

# os.popen("screen python3 ~/Documents/effective-adventure/" + ScriptName)  #os.poopen

