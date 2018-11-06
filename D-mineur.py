from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from kivy.config import Config


class jeu(App):
    def build (self):
        self.title = "Démineur"

        box = BoxLayout(orientation = 'vertical', spacing = 10)


        top = BoxLayout(orientation = 'horizontal', spacing = 10)

        top.add_widget(Button(text = "Time played: ", size=(100, 50), size_hint=(None, None)))
        top.add_widget(Button(text = "Restart ? ", size=(100, 50), size_hint=(None, None)))
        top.add_widget(Button(text = "Play", size=(100, 50), size_hint=(None, None)))

        box.add_widget(top)


        ligne = 16
        colone = 16
        bottom = GridLayout(rows = ligne, cols = colone)
        for i in range(0, colone*ligne):
            self.num = i
            bottom.add_widget(Button())

        box.add_widget(bottom)


        return box



Config.set('graphics', 'width', '400')              #Configuration graphique
Config.set('graphics', 'height', '500')



jeu().run()