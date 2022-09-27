
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   #hide welcome message of pygame
import pygame


class PS4Controller:
    def __init__(self):
        pygame.display.init()
        pygame.joystick.init()
        Joystick = pygame.joystick.Joystick(0)
        Joystick.init()
        self.Joystick = Joystick


    def GetValues(self):

        pygame.event.pump()

        #AXES
        self.LeftStickLR = round(self.Joystick.get_axis(0)*100)
        self.LeftStickUD = round(self.Joystick.get_axis(1)*100)  #between 0 and 100

        self.RightStickLR = round(self.Joystick.get_axis(3)*100)
        self.RightStickUD = round(self.Joystick.get_axis(4)*100)

        self.LeftTrigger = round(self.Joystick.get_axis(2)*100)   #-100 unpressed 100 pressed
        self.RightTrigger = round(self.Joystick.get_axis(5)*100)  #-100 unpressed 100 pressed

        #COMPANSATE PRECISION
        if abs(self.LeftStickLR) < 5 : self.LeftStickLR = 0 
        if abs(self.LeftStickUD) < 5 : self.LeftStickUD = 0
        if abs(self.RightStickLR) < 5 : self.RightStickLR = 0
        if abs(self.RightStickUD) < 5 : self.RightStickUD = 0
        if abs(self.LeftTrigger) < 5 : self.LeftTrigger = 0
        if abs(self.RightTrigger) < 5 : self.RightTrigger = 0

    
        #BUTTONS
        self.CrossButton = self.Joystick.get_button(0)
        self.CircleButton = self.Joystick.get_button(1)
        # self.TriangleButton = self.Joystick.get_button(2)
        # self.SquareButton = self.Joystick.get_button(3)
        # self.LeftBumperButton = self.Joystick.get_button(4)
        # self.RightBumperButton = self.Joystick.get_button(5)
        # self.LeftTiggerPressed = self.Joystick.get_button(6)
        # self.RightTriggerPressed = self.Joystick.get_button(7)
        # self.ShareButton = self.Joystick.get_button(8)
        # self.OptionsButton = self.Joystick.get_button(9)
        # self.PSButton = self.Joystick.get_button(10)
        # self.LefStickIn = self.Joystick.get_button(11)
        # self.RightStickIn = self.Joystick.get_button(12)
  
        #REMAINING BUTTONS
        # D-pad Up        - Button 11
        # D-pad Down      - Button 12
        # D-pad Left      - Button 13
        # D-pad Right     - Button 14
        # Touch Pad Click - Button 15



