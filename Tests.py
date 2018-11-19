from kivy.app import App                           
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.config import Config 
from kivy.uix.widget import Widget

import time
import random
import sys


class jeuApp(App):
    def build(self):
        box = BoxLayout(orientation = 'vertical')
        button = MyButton(ref = [1, 2], id = '3')
        print(button.ref)
        print(button.id)
        box.add_widget(button)
        return box

class MyButton(Button):
    def __init__(self, ref, id):
        super(MyButton, self).__init__()
        self.ref = ref
        self.id = id

jeuApp().run()