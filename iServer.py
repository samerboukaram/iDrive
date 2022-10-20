import zmq
import iOS as iOS
import time
import iBytes as iBY
import pickle


#PUBLISHER CLASS
class Publisher:

    def __init__(self,Host,Port):

         #check and try to kill the PID on the needed Port
        iOS.KillProcessOnPort(int(Port))

        #Create Publisher Socket
        self.Socket = zmq.Context().socket(zmq.PUB)
        self.Socket.bind("tcp://" + Host + ":" + str(Port))


    def PublishImage(self,Topic,Image):

        Data = iBY.EncodeFrame(Image) #encode Image
        Topic = str(Topic).encode('utf-8') # encode topic for sending
        self.Socket.send(Topic+Data)


    # def PublishData(self, Topic, Data): #already encoded

    #     Topic = str(Topic).encode('utf-8') # encode topic for sending
    #     self.Socket.send(Topic+Data)

    # def Publish(self,Topic,Data): 

    #     Topic = str(Topic).encode('utf-8') # encode topic for sending
    #     Data = str(Data).encode('utf-8') # encode topic for sending
    #     self.Socket.send(Topic+Data)


    # def PublishList(self, Topic, Data):
    #     Topic = str(Topic).encode('utf-8') # encode topic for sending
    #     Data = pickle.dumps(Data, 0)
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


# def SubscribeString(Host,Port,Topic):

#     String = Sub(Host,Port,Topic).recv_string()

#     GetTopic = String[0:len(Topic)] #retrieve Topic
#     GetString = String[len(Topic):] #retrive String

#     return GetString


# def SubscribeDataFile(Host,Port,Topic):

#     Socket = zmq.Context().socket(zmq.SUB)
#     Socket.connect ("tcp://" + Host + ":" + str(Port))


#     Socket.setsockopt_string(zmq.SUBSCRIBE,Topic)
#     DataFile = Socket.recv()

#     GetTopic = DataFile[0:len(Topic)].decode('utf-8') #retrieve Topic


#     DataFile  = DataFile[len(Topic):]

#     Data = DataFile[20:] #the first 20 are reserved for time stamp
#     GetData = Data.decode('utf-8')

#     TimeStampData = DataFile[0:20]
#     GetTimeStamp = TimeStampData.decode('utf-8')

#     return GetData, GetTimeStamp



# def SubscribeImageDataFile(Host,Port,Topic):

#     Socket = zmq.Context().socket(zmq.SUB)
#     Socket.connect ("tcp://" + Host + ":" + str(Port))


#     Socket.setsockopt_string(zmq.SUBSCRIBE,Topic)
#     ImageDataFile = Socket.recv()

#     GetTopic = ImageDataFile[0:len(Topic)].decode('utf-8') #retrieve Topic


#     ImageDataFile  = ImageDataFile[len(Topic):]

#     ImageData = ImageDataFile[20:] #the first 20 are reserved for time stamp

#     GetImage = pickle.loads(ImageData, fix_imports=True, encoding="bytes") #retrive Image
#     GetImage = cv2.imdecode(GetImage, cv2.IMREAD_COLOR)

#     TimeStampData = ImageDataFile[0:20]
#     GetTimeStamp = TimeStampData.decode('utf-8')

#     return GetImage, GetTimeStamp

# def SubscribeList(Host,Port,Topic):

#     Socket = zmq.Context().socket(zmq.SUB)
#     Socket.connect ("tcp://" + Host + ":" + str(Port))


#     Socket.setsockopt_string(zmq.SUBSCRIBE,Topic)
#     Data = Socket.recv()

#     GetTopic = Data[0:len(Topic)].decode('utf-8') #retrieve Topic

#     GetList = pickle.loads(Data[len(Topic):], fix_imports=True, encoding="bytes") #retrive Image


#     return GetList



# #to be optimized
# def SubscribeToTwoStrings(Host,Port,Topic1,Topic2):

#     Socket = zmq.Context().socket(zmq.SUB)
#     Socket.connect ("tcp://" + Host + ":" + str(Port))


#     Socket.setsockopt_string(zmq.SUBSCRIBE,Topic1)
#     String = Socket.recv_string()

#     GetTopic = String[0:len(Topic1)] #retrieve Topic
#     GetString1 = String[len(Topic1):] #retrive String


#     Socket.setsockopt_string(zmq.SUBSCRIBE,Topic2)
#     String = Socket.recv_string()

#     GetTopic = String[0:len(Topic2)] #retrieve Topic
#     GetString2 = String[len(Topic2):] #retrive String

#     return GetString1,GetString2







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

    def SendFrame(self, Frame): #needs testing
   
        Data = iBY.EncodeFrame(Frame)
        self.Socket.send(Data) #send the frame


    # def SendFrameDataFile(self, FrameDataFile): #needs testing
   
    #     self.Socket.send(FrameDataFile) #send the frame
    #     Response = self.Socket.recv_string() # must have a response for the server socket to work


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




