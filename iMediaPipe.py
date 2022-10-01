import cv2
import mediapipe as mp
import math



class MediaPipePose:

    def __init__(self):

           self.Pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


    def DetectPose(self, Image):

        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)  
        Image.flags.writeable = False # To improve performance, optionally mark the image as not writeable to pass by reference.
        
        Results = self.Pose.process(Image)
        self.Results = Results
        return Results

        results = pose.process(image)


    #pose must be detected First    
    def DrawPoseOnImage(self, Image, Results):

        # Draw the pose annotation on the image.
        mp.solutions.drawing_utils.draw_landmarks(Image, Results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        self.Image = Image
        return Image 
    


    
    def GetLandMarks(self,number):
        if self.Results.pose_landmarks:
            Landmark = self.Results.pose_landmarks.landmark[number]
            return Landmark.x,Landmark.y, Landmark.z


    def GetCenterOfGravity (self):
        if self.Results.pose_landmarks:
            X, Y, Z = 0, 0 ,0
        
            for Landmark in self.Results.pose_landmarks.landmark:
                X = X + Landmark.x
                Y = Y + Landmark.y
                Z = Z + Landmark.z
            
            Landmarks = len(self.Results.pose_landmarks.landmark)
            print(Landmarks)
            
            X = (X/Landmarks)
            Y = (Y/Landmarks)
            Z = (Z/Landmarks)

            self.Image = cv2.circle(self.Image,(int(self.Image.shape[1]*X),int(self.Image.shape[0]*Y)),10,(0,255,255),-1)
            self.Image = cv2.line(self.Image, (int(self.Image.shape[1]*X),0),(int(self.Image.shape[1]*X),int(self.Image.shape[1])),(0,255,255),2)

            DeltaX = round(X-0.5,2) #postition relative to the center
            self.Image = cv2.putText(self.Image,"DeltaX:" +str(DeltaX), (10,self.Image.shape[0]-50), cv2.FONT_HERSHEY_SIMPLEX, 1,(50,255,255),3,3)


            return DeltaX
            
           

    # use pose_world_landmarks
    def GetShouldersDistance(self):
        if self.Results.pose_landmarks:
            X1,Y1,Z1 = self.GetLandMarks(11) #first Shoulder
            X2,Y2,Z2 = self.GetLandMarks(12) #second Shoulder

            Distance = math.sqrt((X2-X1)**2+(Y2-Y1)**2+(Z2-Z1)**2)
            Distance = round(Distance,2)
            self.Image = cv2.putText(self.Image,"Distance:"+str(Distance), (10,self.Image.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,125,255),3,2)

            return Distance



class MediapieFaceMesh:

    def __init__(self):

           self.FaceMesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)


    def DetectFaceMesh(self, Image):

        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)  
        Image.flags.writeable = False # To improve performance, optionally mark the image as not writeable to pass by reference.
        
        Results = self.FaceMesh.process(Image)
        self.Results = Results
        self.Image = Image
        return Results


    #pose must be detected First    
    def DrawFaceMeshOnImage(self, Image, Results):

        # Draw the pose annotation on the image.
        if Results.multi_face_landmarks:
            for face_landmarks in Results.multi_face_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(Image, landmark_list=face_landmarks, connections= mp.solutions.face_mesh.FACEMESH_TESSELATION, landmark_drawing_spec=None, connection_drawing_spec= mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style())
                mp.solutions.drawing_utils.draw_landmarks(Image, landmark_list=face_landmarks, connections= mp.solutions.face_mesh.FACEMESH_CONTOURS, landmark_drawing_spec=None, connection_drawing_spec= mp.solutions.drawing_styles.get_default_face_mesh_contours_style())


        self.Image = Image
        return Image 
    





#NEEDS TO BE TESTED AND VALIDATED
class MediapipeObjectron:

    def __init__(self):

           self.Objectron = mp.solutions.objectron.Objectron(static_image_mode=False, max_num_objects=5, min_detection_confidence=0.5, min_tracking_confidence=0.99, model_name='Shoe')


    def DetectObjectron(self, Image):

        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)  
        Image.flags.writeable = False # To improve performance, optionally mark the image as not writeable to pass by reference.
        
        Results = self.Objectron.process(Image) 
        self.Results = Results
        self.Image = Image
        return Results


    #pose must be detected First    
    def DrawObjectronOnImage(self, Image, Results):

        # Draw the pose annotation on the image.
        if Results.detected_objects:
            for detected_object in Results.detected_objects:
                mp.solutions.drawing_utils.draw_landmarks(Image, detected_object.landmarks_2d, mp.solutions.objectron.BOX_CONNECTIONS)
                mp.solutions.drawing_utils.draw_axis(Image, detected_object.rotation,detected_object.translation)


        self.Image = Image
        return Image 
    






