from flask import (Flask, render_template, request, Response)
# import time
import cv2


app = Flask(__name__)



def generate_frames(CameraNumber, Width, Height, FPS):

    #Start Camera
    # iOS.KillCamera(self.Number) #kill the camera process if it was already running
    Capture = cv2.VideoCapture(CameraNumber)  # capture video from webcam 0
    Capture.set(cv2.CAP_PROP_FPS, FPS)
    Capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
    Capture.set(cv2.CAP_PROP_FRAME_WIDTH, Width)
    Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, Height)
                              

    while True:

        #Get The Frame    
        Success,frame = Capture.read()
        
        if Success:
            #Encode For Display
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    
        # def Close(self):
    #     # The following frees up resources and closes all windows
    #     self.Capture.release()
    #     cv2.destroyAllWindows()




@app.route('/', methods=['POST','GET'])
def Joystick():

    # t0=  time.time()

    if request.method == "POST":
        Joy1 = request.form["Joy1"]
        print("Joy1", Joy1)
        # print("FPS", round(1/(time.time()-t0)))
        return Joy1 + " Hello"

    return render_template('Joystick.html')


@app.route('/Video')
def Video():
    print("Video")
    return Response(generate_frames(2,640,480,30),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/Video2')
def Video2():
    print("Video2")
    return Response(generate_frames(4,640,480,30),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/Video3')
def Video3():
    print("Video3")
    return Response(generate_frames(0,640,480,30),mimetype='multipart/x-mixed-replace; boundary=frame')


    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)