from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from kivy.config import Config
from kivy.uix.anchorlayout import AnchorLayout
from kivy.base import EventLoop

EventLoop.window.title = "Coucou"

class jeu(App):
    def build (self):
        

        layout = AnchorLayout(anchor_x='left', anchor_y='top')
        btn1 = Button(text='Hello', size_hint = (None, None), size = (100, 400))
        layout.add_widget(btn1)
        return layout





jeu().run()


