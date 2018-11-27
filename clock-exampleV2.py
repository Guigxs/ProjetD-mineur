# Author: Sébastien Combéfis
# Version: November 27, 2018

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label

import random

class TimerApp(App):
    def build(self):
        self.__counter = 0
        Clock.schedule_interval(self._callback, .1)
        
        self.__label = Label(text='', font_size='100sp')
        return self.__label

    def _callback(self, dt):
        Window.top = random.randint(0, 30)
        Window.left = random.randint(0, 20)
        if self.__counter < 10:
            self.__counter += 1
            self.__label.text = str(self.__counter)
            return True
        self.__label.text = 'WIN!!!'
        return False

TimerApp().run()
