import time


def GetTimeStamp(): #in a 20 characters string format
    TimeStamp = str(time.time()) #sensor output time

    while len(TimeStamp)<20:
        TimeStamp = TimeStamp + "0"

    return TimeStamp

def GetTimeStampData(): #encoded
    TimeStamp = GetTimeStamp()    
    TimeStampData = str(TimeStamp).encode('utf-8') # encode topic for sending
    return TimeStampData
 


def t0():
    return time.time()
    
def GetFPS(t0, Display = False):
    tend = time.time()
    FPS = round(1/(tend-t0))

    if Display: print("FPS:", FPS)
    
    return FPS