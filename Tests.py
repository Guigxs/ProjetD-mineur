from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from kivy.config import Config

class jeu(App):
    def build (self):
        self.title = "Démineur"

        layout = BoxLayout(spacing=30)
        btn1 = Button(text='Hello', size=(200, 100), size_hint=(None, None))
        btn2 = Button(text='Kivy', size_hint=(.5, 1))
        btn3 = Button(text='World', size_hint=(.5, 1))
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        return layout






jeu().run()


