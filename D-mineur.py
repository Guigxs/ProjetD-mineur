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


class jeu(App):
    def build (self):
        self.title = "Démineur"                         #titre
        self.icon = "icon.png"

#----------------Boxes haut----------------------
        box = BoxLayout(orientation = 'vertical', size_hint=(None, None), size = (400, 500))       #Boxe generale


        top_box = BoxLayout(orientation='horizontal', size_hint=(1, .1))        #Partie du dessus (top)

        self.sec = 0
        time_box = AnchorLayout(anchor_x='left', anchor_y='top') 
        time_box.add_widget(Label(text = "Time played : {}".format(self.sec), size_hint=(1, 1)))
        top_box.add_widget(time_box)                             # Ajout du temps à la sous-boxe

        
        restart_box = AnchorLayout(anchor_x='center', anchor_y='top')
        self.restart_button = Button(text = "Restart", size_hint=(1, 1))
        self.restart_button.bind(on_release=self._restart)
        restart_box.add_widget(self.restart_button)
        top_box.add_widget(restart_box)                           # Ajout du boutton restart à la sous-boxe


        self.points = 0
        points_box = AnchorLayout(anchor_x='right', anchor_y='top')
        points_box.add_widget(Label(text = "Points : {}".format(self.points), size_hint=(1, 1)))
        top_box.add_widget(points_box)                            # Ajout des points à la sous-boxe

        box.add_widget(top_box)


#------------------ Grille ----------------------
        ligne = 16                                          #Partie du dessous (bottom)
        colonne = 16
        bottom_box = GridLayout(rows = ligne, cols = colonne)
        for self.i in range(0, colonne*ligne):
            self.grid_button = Button(text = str(self.i))
            bottom_box.add_widget(self.grid_button)
            self.grid_button.bind(on_release=self._grid_affichage)


        box.add_widget(bottom_box)
        return box


    def _restart (self, other):                       #opération boutton restart    
        pass

    def _grid_affichage(self, source):              #affichage des case quand on clique
        self.grid_button.background_color = (0, 0, 0, 0)




Config.set('graphics', 'width', '400')              #Configuration graphique de la fenètre
Config.set('graphics', 'height', '500')

jeu().run()