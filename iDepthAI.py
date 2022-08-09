import depthai as dai

#PUBLISHER CLASS
class OakPipelines:

    def __init__(self, RGB= False, MonoLeft = False, MonoRight =  False, Disparity = False, NN = False, VIO = False):
        
        # Start defining a pipeline
        self.Pipeline = dai.Pipeline()

        #Conditions for Node
        if Disparity:
            MonoLeft, MonoRight = True, True



        ###NODE FUNCTIONS

        if RGB:

            # RGB PREVIEW NODE
            self.RGBNode = self.Pipeline.create(dai.node.ColorCamera)
            self.RGBNode.setPreviewSize(640, 480) #300, 300)       
            self.RGBNode.setInterleaved(False)
            self.RGBNode.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
            self.RGBNode.setFps(30)
            self.RGBNode.initialControl.setManualFocus(130)  # For now, RGB needs fixed focus to properly align with depth. # This value was used during calibration

 
            # OutPUT STREAM NODE
            self.RGBOutNode = self.Pipeline.create(dai.node.XLinkOut)
            self.RGBOutNode.setStreamName('RGB')

            #LINK NODES
            self.RGBNode.preview.link(self.RGBOutNode.input)



        if MonoLeft:

            # Define sources and outputs
            self.MonoLeftNode = self.Pipeline.create(dai.node.MonoCamera)
            # Properties
            self.MonoLeftNode.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P) #THE_720_P
            self.MonoLeftNode.setBoardSocket(dai.CameraBoardSocket.LEFT) 
            
            #Output Stream Node
            self.MonoLeftOutNode = self.Pipeline.create(dai.node.XLinkOut)
            self.MonoLeftOutNode.setStreamName('MonoLeft')

            #Link Nodes
            self.MonoLeftNode.out.link(self.MonoLeftOutNode.input)
          
     

    
        if MonoRight:
            # Define sources and outputs
            self.MonoRightNode = self.Pipeline.create(dai.node.MonoCamera)
            # Properties
            self.MonoRightNode.setBoardSocket(dai.CameraBoardSocket.RIGHT)
            self.MonoRightNode.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P) #THE_720_P

            #Output Stream Node
            self.MonoRightOutNode = self.Pipeline.create(dai.node.XLinkOut)
            self.MonoRightOutNode.setStreamName('MonoRight')

            #Link Nodes
            self.MonoRightNode.out.link(self.MonoRightOutNode.input)


        if Disparity:

            self.DepthNode = self.Pipeline.create(dai.node.StereoDepth)
            # Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
            self.DepthNode.initialConfig.setConfidenceThreshold(245)
            
            self.DepthNode.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7) # Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
            self.DepthNode.setLeftRightCheck(False)
            self.DepthNode.setExtendedDisparity(False)
            self.DepthNode.setSubpixel(False)

            self.DepthOutNode = self.Pipeline.create(dai.node.XLinkOut)
            self.DepthOutNode.setStreamName("Disparity")

            #Linking
            self.MonoLeftNode.out.link(self.DepthNode.left)
            self.MonoRightNode.out.link(self.DepthNode.right)
            self.DepthNode.disparity.link(self.DepthOutNode.input)



        if NN:
                # MobilenetSSD label texts
            labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
                        "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


            self.nnNode = self.Pipeline.create(dai.node.MobileNetDetectionNetwork)

            self.nnNode.setConfidenceThreshold(0.5)
            self.nnNode.setBlobPath('/home/interdrive/Documents/cautious-pancake/models/mobilenet-ssd_openvino_2021.2_6shave.blob')
            self.nnNode.setNumInferenceThreads(2)
            self.nnNode.input.setBlocking(False)

        
            self.nnOutNode = self.Pipeline.create(dai.node.XLinkOut)
            self.nnOutNode.setStreamName("nn")

            #Linking
            self.RGBNode.preview.link(self.nnNode.input)
            self.nnNode.out.link(self.nnOutNode.input)
        




        #LINK PIPELINE TO DEVICE
        # Pipeline defined, now the device is assigned and pipeline is started
        self.Device = dai.Device(self.Pipeline)

        #Device Properties
        print('MxId:',self.Device.getDeviceInfo().getMxId())
        print('Connected cameras: ', self.Device.getConnectedCameras())
        print('Usb speed: ', self.Device.getUsbSpeed().name)

    
    def Close(self):
        self.Device.close()   



    ### READING FUNCTIONS

    #also FPS
    def GetFrame(self, StreamName, Frame, FrameTS): #used in a while true loop

        NewFrame, NewFrameTS, FPS = None, None, 0
        Output = self.Device.getOutputQueue(StreamName, 4, blocking=False).tryGet() #tryGet() is non-blocking instead of Get()
       
        if Output:
            NewFrame = Output.getCvFrame()
            NewFrameTS = Output.getTimestamp().total_seconds()
            # FPS = round(1/(NewFrameTS-FrameTS))
        else:
            NewFrame = Frame

        return NewFrame, NewFrameTS #, FPS



    def GetNN(self, X, Y, Percentage, nnTS):
        
        NewX,NewY,NewPercentage = X, Y, Percentage
        Output = self.Device.getOutputQueue("nn", 8).tryGet()

        if Output:
            Detections = Output.detections


            for Detection in Detections:
                DetectionPercentage = round(Detection.confidence*100)
                DetectionX = round((Detection.xmin+Detection.xmax)/2, 3)
                DetectionY = round((Detection.ymin+Detection.ymax)/2, 3)

                # print(Detection.label, Percentage)
                if Detection.label ==15 and DetectionPercentage > 80:
                    NewX,NewY,NewPercentage = DetectionX, DetectionY, DetectionPercentage

        #NewnnTS = Output.getTimestamp().total_seconds()
        #FPS = round(1/(NewnnTS-nnTS))
  
        return NewX, NewY, NewPercentage 







################


    # def NormalizeDisparityFrame(self, Frame):
    #     # Normalization for better visualization
    #     Frame = (Frame * (255 / self.DepthNode.initialConfig.getMaxDisparity())).astype(np.uint8)


    #     # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
    #     Frame = cv2.applyColorMap(Frame, cv2.COLORMAP_JET)
    #     return Frame






 



            # XData = str(X).encode('utf-8') # encode topic for sending
            # # #Save Data
            # iZMQ.SaveData(XData, "Data/X")

            




###########################3
    # if self.VIOSession.hasOutput():

    #         JSONData = self.VIOSession.getOutput().asJson()
    #         print(JSONData)
            
            # #Loads JSON To variables
            # import json
            # VIOData = json.loads(JSONData)

            # OriW = VIOData['orientation']['w']
            # OriX = VIOData['orientation']['x']
            # OriY = VIOData['orientation']['y']
            # OriZ = VIOData['orientation']['z']

            # PosiX = VIOData['position']['x']
            # PosiY = VIOData['position']['y']
            # PosiZ = VIOData['position']['z']
            
            # Status = VIOData['position']
            # Time = VIOData['time']

            # VelocityX = VIOData['velocity']['x']
            # VelocityX = VIOData['velocity']['y']
            # VelocityX = VIOData['velocity']['z']

 