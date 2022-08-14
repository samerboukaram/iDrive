import os

#Use No Hang Up to run Scripts


#Start Camera
os.system("nohup python3 ~/Documents/iDrive/pCamera.py -0 &")

#Stream Camera
os.system("nohup python3 ~/Documents/iDrive/pFlaskCamera.py &")

# os.popen("screen python3 ~/Documents/effective-adventure/" + ScriptName)  #os.poopen

