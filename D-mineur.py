from kivy.app import App                            #LIBRAIRIES KIVY
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.config import Config                         #AUTRES LIBRAIRIES 
from time import *


class jeu(App): 
    def build (self):
        self.title = "Démineur"                         #titre
        self.icon = "icon.png"

#----------------Boxes----------------------
        box = BoxLayout(orientation = 'vertical', size_hint=(None, None), size = (400, 500))       #Boxe generale


        top_box = BoxLayout(orientation='horizontal', size_hint=(1, .1))        #Partie du dessus (top)


        self.time = 0 
        time_box = AnchorLayout(anchor_x='left', anchor_y='top') 
        time_box.add_widget(Button(text = "Time played : {}".format(self.time), size_hint=(1, 1)))
        top_box.add_widget(time_box)                             # Ajout du temps à la sous-boxe

        restart_box = AnchorLayout(anchor_x='center', anchor_y='top')
        restart_box.add_widget(Button(text = "Restart", size_hint=(1, 1)))
        top_box.add_widget(restart_box)                           # Ajout du boutton restart à la sous-boxe


        _points = 0
        points_box = AnchorLayout(anchor_x='right', anchor_y='top')
        points_box.add_widget(Button(text = "Points : {}".format(_points), size_hint=(1, 1)))
        top_box.add_widget(points_box)                            # Ajout des points à la sous-boxe

        box.add_widget(top_box)


#------------------ Grille ----------------------
        ligne = 16                                          #Partie du dessous (bottom)
        colone = 16
        bottom_box = GridLayout(rows = ligne, cols = colone)
        for i in range(0, colone*ligne):
            self.num = i
            bottom_box.add_widget(Button())

        box.add_widget(bottom_box)


        return box

    def _timing(self):
        self.time = int(clock())



Config.set('graphics', 'width', '400')              #Configuration graphique
Config.set('graphics', 'height', '500')



jeu().run()