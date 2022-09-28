
import os
import pprint
import pygame




controller = None
axis_data = None
button_data = None
hat_data = None


"""Initialize the joystick components"""

pygame.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()


"""Listen for events to happen"""

if not axis_data:
    axis_data = {}

if not button_data:
    button_data = {}
    for i in range(controller.get_numbuttons()):
        button_data[i] = False

if not hat_data:
    hat_data = {}
    for i in range(controller.get_numhats()):
        hat_data[i] = (0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axis_data[event.axis] = round(event.value,2)
        elif event.type == pygame.JOYBUTTONDOWN:
            button_data[event.button] = True
        elif event.type == pygame.JOYBUTTONUP:
            button_data[event.button] = False
        elif event.type == pygame.JOYHATMOTION:
            hat_data[event.hat] = event.value

        # Insert your code on what you would like to happen for each event here!
        # In the current setup, I have the state simply printing out to the screen.
        
        os.system('clear')
        pprint.pprint(button_data)
        pprint.pprint(axis_data)
        pprint.pprint(hat_data)


