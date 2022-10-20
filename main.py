__version__ = "1.0.0" #version added to be used by buildozer

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from kivy.uix.widget import Widget
from kivy.clock import Clock

class TouchInput(Widget):

    #introduce variables here, without using self, then call them with self in the functions
    Response = (0, 0)

    def on_touch_down(self, touch):
        self.Response = touch.pos
    def on_touch_move(self, touch):
        self.Response = touch.pos
    def on_touch_up(self, touch):
        self.Response = touch.pos



class SayHello(App):
    def build(self):

        #returns a window object with all it's widgets
        self.window = GridLayout()

        # label widget
        self.Label = Label(text = "nothing")
        self.window.add_widget(self.Label)

        self.Touch = TouchInput()
        self.window.add_widget(self.Touch)


        #Clock
        Clock.schedule_interval(self.ClockFunction, 1.0/100.0)


        return self.window


    def ClockFunction(self, dt):
        self.Label.text = str(int(self.Touch.Response[0])) + "," + str(int(self.Touch.Response[1]))



# run Say Hello App Calss
if __name__ == "__main__":
    SayHello().run()





    