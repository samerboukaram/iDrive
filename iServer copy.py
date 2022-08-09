import zmq
import iOS as iOS
import time
import iBytes as iBY
import pickle


#PUBLISHER CLASS
class Publisher:

    def __init__(self,Port):

        Host = '0.0.0.0' #publish Locally by default

        #check and try to kill the PID on the needed Port
        iOS.KillProcessOnPort(int(Port))
        time.sleep(0.01)
        iOS.KillProcessOnPort(int(Port))
        time.sleep(0.01) #wait no to have a runtime error

        #Create Publisher Socket
        self.Socket = zmq.Context().socket(zmq.PUB)
        self.Socket.bind("tcp://" + Host + ":" + str(Port))


    def Publish(self,Input):

        if type(Input) == 'Numpy array'
        Data = iBY.EncodeFrame(Input) #encode Image
        Topic = str(Topic).encode('utf-8') # Topic is needed for subscribing
        self.Socket.send(Topic+Data)


    # def Publish(self,Topic,Data): 

    #     Topic = str(Topic).encode('utf-8') # encode topic for sending
    #     Data = str(Data).encode('utf-8') # encode topic for sending
    #     self.Socket.send(Topic+Data)





#SUBSCRIBER FUNCTIONS    
def Sub(Host,Port,Topic): #Creates a subscriber
    Sub = zmq.Context().socket(zmq.SUB)
    Sub.connect ("tcp://" + Host + ":" + str(Port))
    Sub.setsockopt_string(zmq.SUBSCRIBE,Topic)
    return Sub


def SubscribeImage(Host,Port,Topic):


    FrameData = Sub(Host,Port,Topic).recv()

    GetTopic = FrameData[0:len(Topic)].decode('utf-8') #retrieve Topic
    GetImage = iBY.DecodeFrame(FrameData[len(Topic):])

    return GetImage






#SERVER CLASS
class Server:

    def __init__(self,Host,Port):

        #check and try to kill the PID on the needed Port
        iOS.KillProcessOnPort(int(Port))
        iOS.KillProcessOnPort(int(Port))
        time.sleep(0.01) #wait no to have a runtime error
        
      
        # REQ and REP archetypes obey a two-step dance of 
        # .send()-.recv()-.send()-.recv()-... and .recv()-.send()-.recv()-... respectively
        self.Socket = zmq.Context().socket(zmq.REP) 
        self.Socket.bind("tcp://" + Host + ":" + str(Port))

    def ReceiveString(self):
        #  Wait for next request from client
        # Message = self.Socket.recv().decode("utf-8") 
        Message = self.Socket.recv_string()
        self.Socket.send_string("thankyousomuch")
        return Message

    def ReceiveMessage(self):
        #  Wait for next request from client
        Data = self.Socket.recv()
        Message = pickle.loads(Data, fix_imports=True, encoding="bytes") 
        self.Socket.send_string("thankyousomuch")

        return Message

    # def ReceiveFrame(self):
    #     #  Wait for next request from client
    #     TimeStamp = self.ReceiveString()
    #     Data = self.Socket.recv()
    #     Frame = pickle.loads(Data, fix_imports=True, encoding="bytes") 
    #     Frame = cv2.imdecode(Frame, cv2.IMREAD_COLOR)
    #     self.Socket.send_string("thankyousomuch")

    #     return Frame, TimeStamp

    def ReceiveFrameData(self):
        #  Wait for next request from client
        TimeStamp = self.ReceiveString()
        Data = self.Socket.recv()
        self.Socket.send_string("thankyousomuch")
        
        return Data, TimeStamp

    def ReceiveFrameDataFile(self):
        #  Wait for next request from client
        Data = self.Socket.recv()
        self.Socket.send_string("thankyousomuch")
        
        return Data

    def SendDataFile(self, Data):
        #  Wait for next request from client
        self.Socket.recv()
        self.Socket.send(Data)
        


    def ReplyToClient(self, Message):
        #  Send reply back to client
        self.Socket.send_string(Message)





#CLIENT CLASS
class Client:
    def __init__(self,Host,Port):
        #save the values
        self.Host = Host
        self.Port = Port
        self.Socket = zmq.Context().socket(zmq.REQ)
        self.Socket.connect("tcp://" + Host + ":" + str(Port))

    def SendString(self, Message):
        self.Socket.send_string(Message)

    def Send(self, Message):
        Data = pickle.dumps(Message, 0) 
        self.Socket.send(Data)

    # def SendFrame(self, Frame, TimeStamp): #needs testing
   
    #     result, frame = cv2.imencode('.jpg', Frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    #     Data = pickle.dumps(frame, 0)
    #     print("Length of the Data", len(Data))


    #     self.SendString(str(TimeStamp))  # send the time stamp first
    #     Response = self.Socket.recv_string() # must have a response for the server socket to work

    #     self.Socket.send(Data) #send the frame


    def SendFrameDataFile(self, FrameDataFile): #needs testing
   
        self.Socket.send(FrameDataFile) #send the frame
        Response = self.Socket.recv_string() # must have a response for the server socket to work

    # def ReceiveDataFile(self):
    #     self.Socket.send_string("Send Please") #send the frame
    #     ImageDataFile = self.Socket.recv() # must have a response for the server socket to work

    #     ImageData = ImageDataFile[20:] #the first 20 are reserved for time stamp

    #     GetImage = pickle.loads(ImageData, fix_imports=True, encoding="bytes") #retrive Image
    #     GetImage = cv2.imdecode(GetImage, cv2.IMREAD_COLOR)

    #     TimeStampData = ImageDataFile[0:20]
    #     GetTimeStamp = TimeStampData.decode('utf-8')

    #     return GetImage, GetTimeStamp

 
    def GetReplyFromServer(self):
        Message = self.Socket.recv().decode("utf-8") 
        return Message




