from flask import (Flask, render_template, request, Response)
# import time
# import iGstreamer2 as iGST


app = Flask(__name__)


import socket
HOST='0.0.0.0'
# PORT = 1234

#Capture Stream from gstreamer through sockets TCP
def GetFramesFromStream(CameraNumber):

    print("CameraNumber", CameraNumber)
    #Start camera
    # Stream=iGST.Pipeline(CameraNumber, "tcpserversink") TODO: could not start here because it stops the running thread
    PORT = 2000+CameraNumber
    print(PORT)

    data = b''
    while True:

        #Socket MUST BE DECLARED INSIDE THE WHILE LOOP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        s.connect((HOST, PORT))

        # t0 = iT.t0()
        data = s.recv(65507) #60000
        print(HOST,PORT)
        yield(b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')


#Capture Stream from gstreamer through sockets UDP
def GetFramesFromStream2(CameraNumber):
    IP = "127.0.0.1"
    PORT = 5005
    print("receiving udp")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((IP, PORT))

    while True:
        print("loopingUDP")
        data = sock.recv(65507)#60000 #65507 #max packet length for udp
        print("done", len(data),HOST,PORT)
        yield(b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')




@app.route('/', methods=['POST','GET'])
def Joystick():

    # t0=  time.time()

    if request.method == "POST":
        Joy1 = request.form["Joy1"]
        # print("Joy1", Joy1)
        # print("FPS", round(1/(time.time()-t0)))
        return Joy1 + " Hello"

    return render_template('Joystick.html')



@app.route('/Video')
def Video():
    print("Video")
    # return "a"
    return Response(GetFramesFromStream2(2),mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/Video2')
def Video2():
    print("Video2")
    return "a"
    # return Response(GetFramesFromStream(0),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/Video3')
def Video3():
    print("Video3")
    return "a"
    # return Response(GetFramesFromStream(4),mimetype='multipart/x-mixed-replace; boundary=frame')


    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)