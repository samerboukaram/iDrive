from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox


def on_checkbox_active(checkbox, value):
    if value:
        print('The checkbox', checkbox, 'is active')
    else:
        print('The checkbox', checkbox, 'is inactive')


import iOS as iSP


import iCamera as iCAM




#Colors
ColorOFF = 'black'
ColorON =  '00FFCE' #'lightgreen'
ColorRefresh = 'green'
ColorDriveButtons = 'blue'





class CameraBox(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraBox, self).__init__(**kwargs)  #inherit the methods of Boxlayout

        self.orientation = "vertical"


        #Refresh Button
        KivyButton = Button(text= "Refresh", size_hint= (1,0.25), bold= False, background_color = 'green')
        KivyButton.bind(on_press=self.Refresh)
        self.add_widget(KivyButton)
        
        #Ttitle
        self.add_widget(KivyLabel("Cameras"))

        # #Cameras
        # ButtonTexts = iCAM.GetCamerasNumbersAndNames()[1]
        # self.ControlBox = GridLayout(cols =3)
        # for ButtonText in ButtonTexts:            
        #     MyButton = Button(text= ButtonText) #create a button
        #     MyButton.bind(on_press=self.ButtonPress)  #bind it to function
        #     self.ControlBox.add_widget(MyButton) #add button to box
        # self.add_widget(self.ControlBox)
   

        #Camera Line
        ButtonTexts = iCAM.GetCamerasNumbersAndNames()[1]
        self.ControlBox = GridLayout(cols =1)
        for ButtonText in ButtonTexts:            
            MyButton = Button(text= ButtonText) #create a button
            MyButton.bind(on_press=self.ButtonPress)  #bind it to function
            self.ControlBox.add_widget(MyButton) #add button to box

            MyLabel = Label(text= 'Port', size_hint= (1,0.25), font_size= 20)
            self.ControlBox.add_widget(MyLabel)

            checkbox = CheckBox()
            checkbox.bind(active=on_checkbox_active)
            self.ControlBox.add_widget(checkbox)

            checkbox = CheckBox()
            checkbox.bind(active=on_checkbox_active)
            self.ControlBox.add_widget(checkbox)
            
        self.add_widget(self.ControlBox)


    def ButtonPress(self, Button): #handle button press
        print('here')
        print(Button.text)
        print(Button.parent)
        # iSP.SwitchProcess(Instance.text)
        self.RefreshColors()



        #Button
    def Refresh(self, Button):
        print(Button.text)







class PublishersBox(BoxLayout):
    def __init__(self, **kwargs):
        super(PublishersBox, self).__init__(**kwargs)  #inherit the methods of Boxlayout

        self.orientation = "vertical"

        #Refresh Button
        KivyButton = Button(text= "Refresh", size_hint= (1,0.25), bold= False, background_color = 'green')
        KivyButton.bind(on_press=self.RefreshButton)
        self.add_widget(KivyButton)
        
        #Ttitle
        self.add_widget(KivyLabel("Publishers"))

        #PUblishers
        ButtonTexts = iSP.GetAllPublishers()
        self.ControlBox = GridLayout(cols =3)
        self.Buttons = []
        for ButtonText in ButtonTexts:            
            MyButton = Button(text= ButtonText) #create a button
            MyButton.bind(on_press=self.ButtonPress)  #bind it to function
            self.Buttons.append(MyButton)
            self.ControlBox.add_widget(MyButton) #add button to box
        self.add_widget(self.ControlBox)

        #Update Colors
        self.RefreshColors()
   

    def ButtonPress(self, Instance):
        
        iSP.SwitchProcess(Instance.text)
        self.RefreshColors()
 
        #refresh colors
    def RefreshButton(self, Button):
        self.RefreshColors()


    def RefreshColors(self):
        for button in self.Buttons:
            Status, PIDList = iSP.CheckIfRunning(button.text)
            if Status: color = ColorON
            else: color = ColorOFF
            button.background_color  = color








class DrivingBox(BoxLayout):
    def __init__(self, **kwargs):
        super(DrivingBox, self).__init__(**kwargs)
        
        self.orientation = 'vertical'

        ColorDriveButtons = 'blue'

        #Driving BOx


        self.ForwardButton = Button(text= 'Forward', background_color = ColorDriveButtons)
        # self.ForwardButton.bind(on_press=self.ForwardPress)
        self.add_widget(self.ForwardButton) #add buttons to window

        self.SteeringBOx = BoxLayout(orientation = 'horizontal')

        self.LeftButton = Button(text= 'Left', background_color = ColorDriveButtons)
        # self.LeftButton.bind(on_press=self.LeftPress)
        self.SteeringBOx.add_widget(self.LeftButton) #add buttons to window

        self.RightButton = Button(text= 'Right', background_color = ColorDriveButtons)
        # self.RightButton.bind(on_press=self.RightPress)
        self.SteeringBOx.add_widget(self.RightButton) #add buttons to window

        self.add_widget(self.SteeringBOx)
        
        self.BackButton = Button(text= 'Back', background_color = ColorDriveButtons)
        # self.BackButton.bind(on_press=self.BackPress)
        self.add_widget(self.BackButton) #add buttons to window


    def RealTime(self):

        if self.ForwardButton.state == 'down':
            print("Forward")
        
        if self.LeftButton.state == 'down':
            print("Left")

        if self.RightButton.state == 'down':
            print("Right")

        if self.BackButton.state == 'down':
            print("Back")

  





#WIDGETS
# Main Window
def KivyMainwindow():
    MainWindow = BoxLayout(orientation ='vertical')
    return MainWindow


#CreateLabel
def KivyLabel(Text):
    KivyLabel = Label(text= Text, size_hint= (1,0.25), font_size= 20)
    return KivyLabel








from kivy.app import App
from kivy.clock import Clock




if __name__=="__main__":
    class iApp(App):
        def build(self):
            self.title = "Cameras"

            #Create Main Window
            self.MainWindow = KivyMainwindow()

            #Add Cameras Box
            self.CameraBox = CameraBox()
            self.MainWindow.add_widget(self.CameraBox)

            self.DrivingBox = DrivingBox()
            self.MainWindow.add_widget(self.DrivingBox)

            self.PublishersBox = PublishersBox()
            self.MainWindow.add_widget(self.PublishersBox)

            #Clock
            Clock.schedule_interval(self.ClockFunction, 1.0/100.0)

            return self.MainWindow


        def ClockFunction(self, dt):
            print("FPS", str(round(1/dt)))

            self.DrivingBox.RealTime()

   
    iApp().run()



