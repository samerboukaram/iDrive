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
     
 
        self.SinkRadio = self.CreateRadioGroup("Sink", ("autovideosink", "tcpserver"))


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

        # self.JPEGCaps = Gst.ElementFactory.make("capsfilter", "CameraFilter")
        # self.JPEGCaps.set_property("caps",  Gst.Caps.from_string("image/jpeg, width=" + str(self.Width) + ", height=" + str(self.Height) + ", framerate=" +self.Framerate))  #format=MJPEG
        # self.AddPipeLine(self.JPEGCaps)


        # # #queue
        # self.queue = Gst.ElementFactory.make("queue", "queue00") #Gtk
        # self.AddPipeLine(self.queue)


        #JPEG DEC
        self.JPEGDec = Gst.ElementFactory.make("jpegdec", "jpegdecoder") #Gtk
        self.AddPipeLine(self.JPEGDec)

        
        #Sink
        #GET SINK TYPE
        self.SinkType = self.GetSelectedRadio(self.SinkRadio)

        #default sink
        # self.Sink = Gst.ElementFactory.make("fakesink", "video-output") #Gtk
        self.Sink = Gst.ElementFactory.make("autovideosink", "video-output") #Gtk
        # self.Sink = Gst.ElementFactory.make("xvimagesink", "video-output") #Gtk
        
        if self.SinkType == "tcpserversink":
            # tcpserversink
            self.Sink = Gst.ElementFactory.make("tcpserversink", "sync to serial port")
            self.Sink.set_property("host", '0.0.0.0')
            self.Sink.set_property("port", 2000)
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


  
