import pickle
import cv2



def EncodeFrame(Frame):
        Result, Frame = cv2.imencode('.jpg', Frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        FrameData = pickle.dumps(Frame, 0)
        # print("Length of frame data", len(FrameData))

        return FrameData

def DecodeFrame(FrameData):

    Frame = pickle.loads(FrameData, fix_imports=True, encoding="bytes") #retrive Image
    Frame = cv2.imdecode(Frame, cv2.IMREAD_COLOR)
    
    return Frame
  
def EncodeString(String):
    StringData = str(String).encode('utf-8')
    
    return StringData

def DecodeString(StringData):

    String = StringData.decode('utf-8')   
    return String


def EncodeInt(Int):
    IntData = Int.to_bytes(3, 'big',signed =True)
    return IntData




#SAVE AND LOAD DATA FROM FILE
def SaveData(Data,FileName):
    DataFile = open(FileName, 'wb') 
    pickle.dump(Data, DataFile)                   
    DataFile.close() 

def LoadData(FileName):
      # for reading also binary mode is important 
    DataFile = open(FileName, 'rb')      
    Data = pickle.load(DataFile)  
    DataFile.close()     
    return Data

def SaveFrame(Frame, FileName):
    SaveData(EncodeFrame(Frame), FileName)


def LoadFrame(FileName):
    return DecodeFrame(LoadData(FileName))
