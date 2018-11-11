#----------------------------------------------------LIBRAIRIES KIVY


from kivy.app import App                           
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout


#-----------------------------------------------------AUTRES LIBRAIRIES 


from kivy.config import Config                         
import time
import random
import sys

class CustomBoxLayout(BoxLayout):
    pass

class CustomBoxLayoutTop(BoxLayout):
    pass

class CustomGridLayout(GridLayout):
    pass

class CustomButton(Button):
    pass

class JeuDemineurApp(App):
    def build(self):
        box = CustomBoxLayout()


        top_box = CustomBoxLayoutTop()
        self.flags = 3
        box.add_widget(top_box)


        bottom_box = CustomGridLayout()

        for i in range(16*16):
            bottom_box.add_widget(CustomButton())

        box.add_widget(bottom_box)

        return box


jeuDemineur = JeuDemineurApp()
jeuDemineur.run()