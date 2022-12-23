import gi
gi.require_version("Gst", "1.0")
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, Gtk

#GET CAMERAS FROM SYSTEM


class Pipeline:

    def __init__(self, CameraNumber=0, SinkType = "autovideosink") -> None:

        Gst.init(None)  

        #Create Player
        self.Player = Gst.Pipeline.new("player")
        self.LinkList =[] #used to link pipelines

        #Source
        self.source = Gst.ElementFactory.make("v4l2src", "ovideo-source")
        self.source.set_property("device", "/dev/video" + str(CameraNumber))
        self.AddPipeLine(self.source)
        
        #Add Caps
        self.JPEGCaps = Gst.ElementFactory.make("capsfilter", "CameraFilter")
        self.JPEGCaps.set_property("caps",  Gst.Caps.from_string("image/jpeg, format=MJPEG, width=640, height=360, framerate=30/1"))  #format=MJPEG
        self.AddPipeLine(self.JPEGCaps)

        #Sink
        #default sink
        if SinkType =="autovideosink":

            #JPEG DEC
            self.JPEGDec = Gst.ElementFactory.make("jpegdec", "jpegdecoder") #Gtk
            self.AddPipeLine(self.JPEGDec)
  
            #autovideosink
            self.Sink = Gst.ElementFactory.make("autovideosink", "video-output") #Gtk
            self.AddPipeLine(self.Sink)
     
        
        if SinkType == "tcpserversink":
            # tcpserversink
            self.Sink = Gst.ElementFactory.make("tcpserversink", "sync to serial port")
            self.Sink.set_property("host", '0.0.0.0')
            self.Sink.set_property("port", 2000+int(CameraNumber))
            self.AddPipeLine(self.Sink)

        if SinkType == "udpsink":
            # tcpserversink
            self.Sink = Gst.ElementFactory.make("udpsink", "sync to serial port")
            self.Sink.set_property("host", '0.0.0.0')
            self.Sink.set_property("port", 2000+int(CameraNumber))
            self.AddPipeLine(self.Sink)


        #Link PipeLines 
        for i in range(len(self.LinkList)-1): 
            self.LinkList[i].link(self.LinkList[i+1])   


        
                 # Stream = Pipeline()
        self.Player.set_state(Gst.State.PLAYING)


        #Placed to trigger the application
        Gtk.main()
        # Gtk.main_quit #Quit the applicaton

        # Stream.Player.set_state(Gst.State.NULL) #Stop

 
  

    def AddPipeLine(self, Pipeline):
        self.Player.add(Pipeline)
        self.LinkList.append(Pipeline)
        


if __name__ == '__main__':

    OD = Pipeline(CameraNumber=2, SinkType="tcpserversink")
