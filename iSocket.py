#SHOULD BE Totally replaced/merged BY iZMQ

import socket
import pickle
import cv2


def CreateServerSocket(HOST, PORT):
    # Leave Blank for LocalHost
    # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))  # associate socket with Host and port
    s.listen()  # places the server in listening mode  #backlog umber of unaccepted connections that the system will allow before refusing new connections.
    return s


def CreateClientSocket(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s


# USE THIS FOR SERVER ACCEPTING
# conn, addr = s.accept()  #get client socket object conn, and his adress
# print('Connected by', addr)

def ServerReadInt(conn):
    return int.from_bytes(conn.recv(10), 'big')


def ServerReadString(conn):
    return conn.recv(3).decode('utf-8')


#TO BE TESTED
def ServerReadFrame(conn):
    size = ServerReadInt(conn) #get frame size

    frame_data = conn.recv(size)
    while len(frame_data) < size:
        frame_data += conn.recv(4096)

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    return frame


def ServerSendInt(conn, message):
    conn.sendall(message.to_bytes(3, 'big'))


def ServerSendString(conn, message):
    conn.sendall(str(message).encode('utf-8'))


def ServerSendFrame(conn, frame):
    result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    data = pickle.dumps(frame, 0)

    ServerSendInt(conn, len(data))  # send the size first

    conn.sendall(data) #send the frame


def ServerSendSound(conn,data):
    conn.sendall(data) #send the frame


def ServerSendObject(conn,Object):
    ############################
    pass

# CLIENT
def ClientSendInt(s, message):
    s.sendall(message.to_bytes(3, 'big',signed =True))


def ClientSendString(s, message):
    s.sendall(message.encode('utf-8'))


def ClientReadInt(s):
    size =  int.from_bytes(s.recv(3), 'big', signed = True)
    return size


def ClientReadString(s):
    return s.recv(3).decode('utf-8')
    


def ClientReadFrame(s):
    size = ClientReadInt(s) #get frame size

    frame_data = s.recv(size)
    while len(frame_data) < size:
        frame_data += s.recv(4096)

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    try:
     frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    except:
        return None
    return frame


def ClientSendFrame(s,frame):
    result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    data = pickle.dumps(frame, 0)

    ClientSendInt(s, len(data))  # send the size first
    s.sendall(data) #send the frame


#send Bytes
def ClientSendData(s,Data):
    s.sendall(Data)


def ClientReadData(s):
    Data = s.recv(500)
    return Data



def ClientReadSound(s):
    data = s.recv(4096)
    return data




#get a frame from socket
def GetFrameFromSSH(Host, Port):

        #create client Socket
        s = CreateClientSocket(Host,Port)

        #send Request
        ClientSendInt(s,0)  #send a zero for SSH Server to know an image is requested

        #receive Frame
        Frame= ClientReadFrame(s)
        return Frame



#publishes frames to SSH
def PublishFrameToSSH(Frame, Host, Port):

    #create client Socket
    PublisherClientSocket = CreateClientSocket(Host,Port)

    #Send Frame
    try:
        ClientSendFrame(PublisherClientSocket, Frame)
    except:
        print("no frame sent")

