#Start Gstreamer programatically with gi library, and test values of encoder with GUI
import gi
gi.require_version("Gst", "1.0")
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, Gtk

import os

#GET CAMERAS FROM SYSTEM


def GetCameras():

    def GetFirstLineFromFile(FilePath): 
        File = open(FilePath)
        FirstLine = File.read().split('\n')[0]
        File.close()
        return FirstLine


    #Ubuntu 20.04 pathH264Parse
    V4LDIR = "/sys/class/video4linux"

    #initialize lists
    Cameras=[]

    #Get Cameras
    for Video in os.listdir(V4LDIR):

        CameraName = GetFirstLineFromFile(V4LDIR+"/"+Video+"/name")
        CameraIndex = int(GetFirstLineFromFile(V4LDIR+"/"+Video+"/index"))
        CameraNumber = int(Video.split('video')[1]) #get just the number
    
        if CameraIndex == 0:
            Cameras.append((CameraNumber,CameraName))

    return Cameras


def GetCameraNumber(CameraName): #TODO: check that is only returning the frist camera by this name
    for Camera in GetCameras():
        if Camera[1]==CameraName: return Camera[0]


def GetCameraName(CameraNumber):
    for Camera in GetCameras():
        if Camera[0]==CameraNumber: return Camera[1]


#how to get camera resolutions:
#with Gstreamer
#gst-device-monitor-1.0
#With v4l-utils
#v4l2-ctl -d /dev/video0 --list-formats-ext

import cv2
def GetCameraResolutions(CameraNumber): #SOME RESOLUTIONS NOT FOUND FOR 9732 136deg camera!!!

    cap = cv2.VideoCapture(CameraNumber)


    CommonResolutions = ('160x120',
                '176x144',
                '320x240',
                '352x255',
                '640x360',
                '640x480',
                '1280x720',
                )

    resolutions = {}

    for Resolution in CommonResolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(Resolution.split("x")[0]))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(Resolution.split("x")[1]))
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        resolutions[str(width)+"x"+str(height)] = "OK"
    print(resolutions)

# GetCameraResolutions(2)


class GStreamer:

    def __init__(self) -> None:

        Gst.init(None)  

        self.CreateGUI() 

        self.UpdatePlayer()

        try:
            self.UARTLocation = "/dev/ttyUSB0"
            os.system("stty -F " + self.UARTLocation + " raw")
            os.system("stty -F " + self.UARTLocation + " 2500000") #only 2000000 & 25000000
        except:
            print("WARNING: Failed setting up serial port")


    def CreateGUI(self):

        #Main Window
        window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        window.set_title("Videotestsrc-Player")
        window.set_default_size(300, -1)
        window.connect("destroy", Gtk.main_quit, "WM destroy")

        #Main Vertical BOX
        self.vbox = Gtk.VBox()
        window.add(self.vbox)

        #Play Button
        self.button = Gtk.Button(label="Start")
        self.button.connect("clicked", self.start_stop)
        self.vbox.add(self.button)

        #Horizontal Box for Checkboxes
        self.hBoxForCheckboxes = Gtk.HBox()
        self.vbox.add(self.hBoxForCheckboxes)

        #Add GUI elements
        # Cameras = list()
        # for Camera in GetCameras(): Cameras.append(Camera[0])
        # self.CameraNumberRadio = self.CreateRadioGroup("Camera Number", Cameras)
        self.CameraNumberRadio = self.CreateRadioGroup("Camera Number", (0,1,2,3,4,5,6))
        self.ResolutionRadio = self.CreateRadioGroup("Resolution", ("640x360","1280x720","800x600", "640x480", "160x120"))
        self.FramerateRadio = self.CreateRadioGroup("Framerate", (20,10,15,5,25,30))
        self.PassRadio = self.CreateRadioGroup("Pass", (0,5,4,17,18,19))  #maybe this is control rate, 19 pass3 is like control-rate=3
        self.QuantizerSlider = self.CreateSlider("Quantizer", 21, 1,50)
        self.SpeedPresetRadio = self.CreateRadioGroup("Speed Preset", (0,1,2,3,4,5,6,7,8,9,10))
        self.BitrateSlider = self.CreateSlider("Bitrate", 500, 1,3000)
        self.TuneRadio = self.CreateRadioGroup("Tune", ("zerolatency", "fastdecode", "stillimage"))
        # self.ByteStreamCheckBox = self.CreateCheckBox("Byte Stream", True)
        self.IntraRefreshCheckBox = self.CreateCheckBox("Intra-Refresh", True)
        self.submeSlider = self.CreateSlider("subme", 4, 1,10)
        self.CabacCheckBox = self.CreateCheckBox("Cabac", False)
        self.TrellisCheckBox = self.CreateCheckBox("Trellis", False)
        self.dct8x8DCheckBox = self.CreateCheckBox("dct8x8", True)
        self.InterlacedCheckBox = self.CreateCheckBox("Interlaced", False)
        self.ThreadsRadio = self.CreateRadioGroup("Threads", (0,1,2,3,4,5,6,7,8))
        self.keyintmaxSlider = self.CreateSlider("key-int-max", 12, 0,20)
        self.QPminSlider = self.CreateSlider("QPmin", 0, 0,50)
        self.QPmaxSlider = self.CreateSlider("QPmax", 51, 10,51)
        self.QPstepSlider = self.CreateSlider("QPstep", 4, 0,51)
        self.RCLookahedSlider = self.CreateSlider("RC Lookahead", 0, 0,50)
        self.ProfileRadio = self.CreateRadioGroup("Profile", ("constrained-baseline", "baseline", "high","main")) #baseline profiles probably dont have b frames ???
        self.BFramesSlider = self.CreateSlider("Bframes (buffer frames)", 0, 0,16)
        self.SlicedThreadsCheckBox = self.CreateCheckBox("Sliced Threads", True)
        self.MBTreeCheckBox = self.CreateCheckBox("mb-tree", False)
        self.VBVBuffCapacitySlider = self.CreateSlider("vbv-buf-capacity", 0, 0, 5000) #default was 600
        self.MERadio = self.CreateRadioGroup("ME", ("hex","dia","umh","esa","tesa"))
        self.RefSlider = self.CreateSlider("Ref", 3, 1,12)
        self.SyncLookahedSlider = self.CreateSlider("sync Lookahead", 0, -1,250)
        self.PBFactorSlider = self.CreateSlider("PB factor", 10, 0,20)
        self.IPFactorSlider = self.CreateSlider("IP factor", 10, 0,20)
        self.WeightBCheckBox = self.CreateCheckBox("Weight B", False)
        self.AUDBCheckBox = self.CreateCheckBox("AUD", True)
        self.BadaptCheckBox = self.CreateCheckBox("b-adapt", True)
        self.BPyramidCheckBox = self.CreateCheckBox("b-pyramid", False)
        self.InsertVUICheckBox = self.CreateCheckBox("insert-vui", True)
        self.PsyTuneRadio = self.CreateRadioGroup("Psy Tune", (0,1,2,3,4,5))
        self.AnalyseRadio = self.CreateRadioGroup("Analyse", ("None", "i4x4", "i8x8","p8x8","p4x4","b8x8"))
        self.SinkRadio = self.CreateRadioGroup("Sink", ("autovideosink", "UART"))


        #Display Window
        window.show_all()


            
    def UpdatePlayer(self): #TODO: read default values from GUI

        #Stop Player
        if self.button.get_label() == "Stop":
            self.Player.set_state(Gst.State.NULL) #Stop

        #Create Player
        self.Player = Gst.Pipeline.new("player")
        self.LinkList =[] #used to link pipelines

        #Get Values
        self.VideoType = "image/jpeg" #"video/x-raw" "video/x-h264"
        

        
        #v4l2 Source
        self.CameraNumber= self.GetSelectedRadio(self.CameraNumberRadio)

        self.source = Gst.ElementFactory.make("v4l2src", "ovideo-source")
        self.source.set_property("device", "/dev/video" + self.CameraNumber)
        self.AddPipeLine(self.source)
        
        #Add Caps
        Resolution = self.GetSelectedRadio(self.ResolutionRadio)
        self.Width, self.Height =Resolution.split("x")[0], Resolution.split("x")[1]
        # self.Width, self.Height =640,360
        self.Framerate = str(int(self.GetSelectedRadio(self.FramerateRadio))) + "/1"

        self.JPEGCaps = Gst.ElementFactory.make("capsfilter", "CameraFilter")
        self.JPEGCaps.set_property("caps",  Gst.Caps.from_string("image/jpeg, width=" + str(self.Width) + ", height=" + str(self.Height) + ", framerate=" +self.Framerate))  #format=MJPEG
        self.AddPipeLine(self.JPEGCaps)


        # # #queue
        # self.queue = Gst.ElementFactory.make("queue", "queue00") #Gtk
        # self.AddPipeLine(self.queue)


        #JPEG DEC
        self.JPEGDec = Gst.ElementFactory.make("jpegdec", "jpegdecoder") #Gtk
        self.AddPipeLine(self.JPEGDec)

        # #JDecodeBIn
        # self.DecodeBIn = Gst.ElementFactory.make("decodebin", "decodebin") #Gtk
        # self.AddPipeLine(self.DecodeBIn)
        #  #Videoconvert
        # self.VideoConvert = Gst.ElementFactory.make("videoconvert", "VideoConvert0") #Gtk
        # self.AddPipeLine(self.VideoConvert)


      


        #GET SINK TYPE
        self.SinkType = self.GetSelectedRadio(self.SinkRadio)

        if self.SinkType == "UART":


            # #queue
            # self.queue = Gst.ElementFactory.make("queue", "queue0") #Gtk
            # self.AddPipeLine(self.queue)

            # #Videoconvert
            # self.VideoConvert = Gst.ElementFactory.make("videoconvert", "VideoConvert") #Gtk
            # self.AddPipeLine(self.VideoConvert)


            # #queue
            # self.queue = Gst.ElementFactory.make("queue", "queue01") #Gtk
            # self.AddPipeLine(self.queue)

            # self.VideoConCaps = Gst.ElementFactory.make("capsfilter", "videoconvertfilter")
            # self.VideoConCaps.set_property("caps",  Gst.Caps.from_string("video/x-raw, format=I420"))
            # self.AddPipeLine(self.VideoConCaps)

            #queue
            self.queue = Gst.ElementFactory.make("queue", "queue1") #Gtk
            self.AddPipeLine(self.queue)



            # #x264enc
            self.x264enc = Gst.ElementFactory.make("x264enc", "h264-encoder") #Gtk
            self.x264enc.set_property("pass", int(self.GetSelectedRadio(self.PassRadio)))
            self.x264enc.set_property("quantizer", int(self.QuantizerSlider.get_value())) #25
            self.x264enc.set_property("speed-preset", int(self.GetSelectedRadio(self.SpeedPresetRadio)))
            self.x264enc.set_property("bitrate", int(self.BitrateSlider.get_value()))
            self.x264enc.set_property("tune", self.GetSelectedRadio(self.TuneRadio))
            self.x264enc.set_property("byte-stream", True)  #self.ByteStreamCheckBox.get_active()
            self.x264enc.set_property("intra-refresh", int(self.submeSlider.get_value()))
            self.x264enc.set_property("subme", int(self.submeSlider.get_value()))
            self.x264enc.set_property("cabac", self.CabacCheckBox.get_active())
            self.x264enc.set_property("trellis", self.TrellisCheckBox.get_active())
            self.x264enc.set_property("dct8x8", self.dct8x8DCheckBox.get_active())
            self.x264enc.set_property("interlaced", self.InterlacedCheckBox.get_active())
            self.x264enc.set_property("threads", int(self.GetSelectedRadio(self.ThreadsRadio)))
            self.x264enc.set_property("key-int-max", int(self.keyintmaxSlider.get_value()))
            self.x264enc.set_property("qp-min", int(self.QPminSlider.get_value()))
            self.x264enc.set_property("qp-max", int(self.QPmaxSlider.get_value()))
            self.x264enc.set_property("qp-step", int(self.QPstepSlider.get_value()))
            self.x264enc.set_property("rc-lookahead", int(self.RCLookahedSlider.get_value()))
            self.x264enc.set_property("bframes", int(self.BFramesSlider.get_value()))
            self.x264enc.set_property("sliced-threads", self.SlicedThreadsCheckBox.get_active())
            self.x264enc.set_property("mb-tree", self.MBTreeCheckBox.get_active())
            self.x264enc.set_property("vbv-buf-capacity", int(self.VBVBuffCapacitySlider.get_value()))
            self.x264enc.set_property("me", self.GetSelectedRadio(self.MERadio))
            self.x264enc.set_property("ref", int(self.RefSlider.get_value()))
            self.x264enc.set_property("sync-lookahead", int(self.SyncLookahedSlider.get_value()))
            self.x264enc.set_property("pb-factor", int(self.PBFactorSlider.get_value())/10)
            self.x264enc.set_property("ip-factor", int(self.IPFactorSlider.get_value())/10)
            self.x264enc.set_property("weightb", self.WeightBCheckBox.get_active())
            self.x264enc.set_property("aud", self.AUDBCheckBox.get_active())
            self.x264enc.set_property("b-adapt", self.BadaptCheckBox.get_active())
            self.x264enc.set_property("b-pyramid", self.BPyramidCheckBox.get_active())
            self.x264enc.set_property("insert-vui", self.InsertVUICheckBox.get_active())
            self.x264enc.set_property("psy-tune", int(self.GetSelectedRadio(self.PsyTuneRadio)))
            # if self.GetSelectedRadio(self.TuneRadio) != "None":
            #     self.x264enc.set_property("tune", self.GetSelectedRadio(self.TuneRadio))
            self.AddPipeLine(self.x264enc)

            # #queue
            # self.queue = Gst.ElementFactory.make("queue", "queue1.5") #Gtk
            # self.AddPipeLine(self.queue)


            # #Add Caps
            self.x264Caps = Gst.ElementFactory.make("capsfilter", "h264Filter")
            Caps = "video/x-h264,framerate=" +self.Framerate
            Caps = Caps + ",profile=" + self.GetSelectedRadio(self.ProfileRadio)
            Caps = Caps + ",stream-format=byte-stream"  #add bytestream
            self.x264Caps.set_property("caps",  Gst.Caps.from_string(Caps))
            self.AddPipeLine(self.x264Caps)


            # #queue
            # self.queue = Gst.ElementFactory.make("queue", "queue2") #Gtk
            # self.AddPipeLine(self.queue)

            # #H264 Parse
            # self.H264Parse = Gst.ElementFactory.make("h264parse", "parser") #Gtk
            # self.AddPipeLine(self.H264Parse)

            # #queue
            # self.queue = Gst.ElementFactory.make("queue", "queue3") #Gtk
            # self.AddPipeLine(self.queue)

            # #MUX
            # self.MUX = Gst.ElementFactory.make("avimux", "mux") #Gtk
            # self.AddPipeLine(self.MUX)

            # #queue
            # self.queue = Gst.ElementFactory.make("queue", "queue4") #Gtk
            # self.AddPipeLine(self.queue)
        
        #Sink

        #default sink
        # self.Sink = Gst.ElementFactory.make("fakesink", "video-output") #Gtk
        self.Sink = Gst.ElementFactory.make("autovideosink", "video-output") #Gtk
        # self.Sink = Gst.ElementFactory.make("xvimagesink", "video-output") #Gtk
        
        if self.SinkType == "UART":
            # FileSink
            self.Sink = Gst.ElementFactory.make("filesink", "sync to serial port")
            self.Sink.set_property("location", self.UARTLocation)
        self.AddPipeLine(self.Sink)


        #Link PipeLines 
        for i in range(len(self.LinkList)-1): 
            self.LinkList[i].link(self.LinkList[i+1])   

        # print("player updated")


        #Resume player
        if self.button.get_label() == "Stop":
            self.Player.set_state(Gst.State.PLAYING) #Play


    def AddPipeLine(self, Pipeline):
        self.Player.add(Pipeline)
        self.LinkList.append(Pipeline)
        

    ##########Functions to accelerate GUI elements creation
    def CreateRadioGroup(self, Label, Values):
      
        #Add horizontal radio buttons
        hbox = Gtk.HBox()

        #Add label
        hbox.add(Gtk.Label(label=Label))

        i=1
        for value in Values:

            if i==1:
                RadioButton1 = Gtk.RadioButton(label=value)
                RadioButton1.connect("toggled", self.RadioToggle)
                hbox.pack_start(RadioButton1, True, True, 0)
                i=i+1 #only for the first button
            
            else: #add the rest of the buttons to the group
                RadioButton = Gtk.RadioButton(label=value, group=RadioButton1)
                RadioButton.connect("toggled", self.RadioToggle)
                hbox.add(RadioButton)

        #Add radios to the main menu
        self.vbox.add(hbox)
        return RadioButton1


    def CreateSlider(self, Label, DefaultValue, Min, Max):

        #Create a horizontal box
        hbox = Gtk.HBox()
        
        #Add label
        hbox.add(Gtk.Label(label=Label))

        #Add slider
        slider = Gtk.HScale.new_with_range(min=Min, max=Max, step=1)
        slider.set_value(DefaultValue)
        slider.connect("value-changed", self.SliderChange)
        hbox.add(slider)

        #add box to layout
        self.vbox.add(hbox)
        return slider

    def CreateCheckBox(self,Label, Default):

        CheckBox = Gtk.CheckButton(label=Label)
        CheckBox.set_active(Default)
        CheckBox.connect("toggled", self.CheckBoxChange)
        self.hBoxForCheckboxes.add(CheckBox)
        return CheckBox

    


    # FUNCTIONS FOR GUI EVENTS
    def start_stop(self, w):
        if self.button.get_label() == "Start":
            self.button.set_label("Stop")
            self.Player.set_state(Gst.State.PLAYING) #Play
        else:
            self.Player.set_state(Gst.State.NULL) #Stop
            self.button.set_label("Start")


    def RadioToggle(self, RadioButtons):
        self.UpdatePlayer()

    def SliderChange(self, range):
        self.UpdatePlayer()

    def CheckBoxChange(self, checkbox):
        self.UpdatePlayer()

    def GetSelectedRadio(self, RadioButtons): #get selected radio

        for Radio in RadioButtons.get_group():
            if Radio.get_active():
                # print(Radio.get_label())
                return Radio.get_label() #returns the selected radio button




      
    
    # def on_check_button_toggled(self, checkbutton):
    #     if checkbutton.get_active():
    #         print("CheckButton toggled on!")
    #     else:
    #         print("CheckButton toggled off!")







Stream = GStreamer()
Stream.UpdatePlayer()



#Placed to trigger the application
Gtk.main()
Gtk.main_quit #Quit the applicaton


  
