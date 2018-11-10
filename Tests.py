from kivy.app import App                            #LIBRAIRIES KIVY
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

from kivy.config import Config                         #AUTRES LIBRAIRIES 
import time


class jeuApp(App):
    def build (self):

        self.title = "Démineur"                         #titre
        self.icon = "icon.png"

        box = BoxLayout(orientation = 'vertical', size_hint=(None, None), size = (400, 500))       #Boxe generale


        top_box = BoxLayout(orientation='horizontal', size_hint=(1, .1))        #Partie du dessus (top)

        
        time_box = AnchorLayout(anchor_x='left', anchor_y='top') 
        time_box.add_widget(Label(text = "Time played : {}".format("1"), size_hint=(1, 1)))
        top_box.add_widget(time_box)                             # Ajout du temps à la sous-boxe

        box.add_widget(top_box)


        ligne = 3                                          #Partie du dessous (bottom)
        colonne = 3
        bottom_box = GridLayout(rows = ligne, cols = colonne)

        for i in range(ligne*colonne):
            self.v = Button()
            self.v.bind(on_release=self._grid_affichage)
            bottom_box.add_widget(self.v)


        box.add_widget(bottom_box)
        return box

    def _grid_affichage(self, source):              #affichage des case quand on clique
        source.background_normal = ""



Config.set('graphics', 'width', '400')              #Configuration graphique de la fenètre
Config.set('graphics', 'height', '500')


jeu = jeuApp()
jeu.run()