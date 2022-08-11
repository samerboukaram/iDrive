#Requires pCamera.py
from flask import Flask,render_template,Response
import cv2
import iOS as iOS
import time
import iServer


Port = 2021


#check and try to kill the PID on the needed Port
iOS.KillProcessOnPort(int(Port))
iOS.KillProcessOnPort(int(Port))
time.sleep(0.01) #wait no to have a runtime error



#Create App
app=Flask(__name__)

def generate_frames():
    while True:
            
        ## read the camera frame
        frame = iServer.SubscribeImage('0.0.0.0',2000,"CAMERA")
        print('here')
        # iCAM.DisplayFrame(frame)

        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


#Create Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


#Run the APP
app.run(host='0.0.0.0',port=Port,debug=False)