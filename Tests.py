import kivy

from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import NumericProperty

from kivy.lang import Builder

import time

class CrudeTimerGrid(GridLayout):
    time = NumericProperty(0)

    def tick(self, *_):
        if self.time > 0:
            self.time -= 1
        else:
            pass

    def start(self, *_):
        self.cb = Clock.schedule_interval(self.tick,1)

    def pause(self):
        Clock.unschedule(self.cb)

    # incomplete code
    def reset(self, *_):
        pass


class CrudeTimerApp(App):
    def build(self):
        # Testing timer by initialising timer with 20 seconds
        return CrudeTimerGrid(time=20)

Builder.load_string('''
<CrudeTimerGrid>
    id: timer
    rows: 2
    # insert formatting here

    BoxLayout:
        Label:
            text: str(timer.time)

    BoxLayout:

        Button:
            text: "Start"
            on_press: timer.start()

        Button:
            text: "Pause"
            on_press: timer.pause()

        Button:
            text: "Reset"
            on_press: timer.reset()
''')

CrudeTimerApp().run()