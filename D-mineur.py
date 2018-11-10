from kivy.app import App                            #LIBRAIRIES KIVY
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock


#-----------------------------------------------------


from kivy.config import Config                         #AUTRES LIBRAIRIES 
import time
import random
import sys


class jeuApp(App):

    def build (self):

        self.title = "Démineur"                         #titre
        self.icon = "images/icon.png"                          #image

        self.ligne = 16                                 #initialisation des variables
        self.colonne = 16

        self.Lligne=[]
        self.Ltotale=[]

        self.drapeau = 28


        self.random_list_x =[]
        self.random_list_y=[]


#----------------Generation des bombes aleatoirement---------------


        for r in range(14):#Selon les x
            self.random_list_x.append(random.randrange(16))

        for s in range(14):#Selon les y
            self.random_list_y.append(random.randrange(16))


#----------------Boxes haut----------------------


        box = BoxLayout(orientation = 'vertical', size_hint=(None, None), size = (400, 500))       #Boxe generale


        top_box = BoxLayout(orientation='horizontal', size_hint=(1, .1))        #Partie du dessus (top)

        
        
        time_box = AnchorLayout(anchor_x='left', anchor_y='top') 
        time_box.add_widget(Label(text = "Time played : {}".format("0"), size_hint=(1, 1)))
        top_box.add_widget(time_box)                             # Ajout du temps à la sous-boxe

        
        restart_box = AnchorLayout(anchor_x='center', anchor_y='top')
        self.restart_button = Button(text = "Restart", size_hint=(1, 1))
        self.restart_button.bind(on_release=self._restart)
        restart_box.add_widget(self.restart_button)
        top_box.add_widget(restart_box)                        # Ajout du boutton restart à la sous-boxe


        points_box = AnchorLayout(anchor_x='right', anchor_y='top')
        self.counting_points = Label(text = "Flags : 28", size_hint=(1, 1))
        points_box.add_widget(self.counting_points)
        top_box.add_widget(points_box)                            # Ajout des points à la sous-boxe

        box.add_widget(top_box)


#------------------ Grille ----------------------
            

        bottom_box = GridLayout(rows = self.ligne, cols = self.colonne)       #Partie du dessous (bottom)
        with open("data.txt", "w") as file:

            for self.i in range(self.ligne):#On repete l'action pour chaque lignes          
                for self.e in range(self.colonne):#On répete l'action pour chaque colonnes
                    self.grid_button = Button(background_down = "images/gris.png")#Quand on enfonce le bouton 
                    self.grid_button.bind(on_release=self._grid_affichage)#Appel la méthode pour réveler la case
                    self.grid_button.bind(on_press=self._drapeau)#Appel la methode pour afficher les drapeaux et compter les points
                    self.grid_button.bind(on_release=self._compare)#Appel la methode pour veriffier si on est pas sur une bombe
                    bottom_box.add_widget(self.grid_button)
                    self.Lligne.append(self.e)#ajout du chiffre (e) dans la sous-liste Lligne 
                self.Ltotale.append(self.Lligne)#Ajoute la liste dans la liste Ltitals
                self.Lligne =[]#Remise à 0 de la sous-liste Lligne pour recommencer
            file.write(str(self.Ltotale))#Ecrit la liste Ltotale dans data.txt
        

        box.add_widget(bottom_box)
        return box


#------------- Boucles évenementielles -------------------------


    def _timer (self):                              #chronometre
        pass


    def _restart (self, other):                       #opération boutton restart    
        pass


    def _drapeau (self, source):                        #Affichage des drapeaux et des points
        source.background_normal = "images/drapeau.png"        #Change le background en drapeau 
        self.drapeau -= 1                               #Change les points (Départ de 28 -> 0)
        self.counting_points.text = "Flags : " + str(self.drapeau)


    def _grid_affichage(self, source):              #affichage des cases quand on clique
        source.background_normal = "images/gris.png"


    def _compare(self, source):                         #test si on clique sur une bombe

        if str(source) == str(3):                 #quitte le jeu si on clique sur une bombe
            sys.exit(0)
        else:
            pass



#-------------------------Fin de la class----------------------------


Config.set('graphics', 'width', '400')              #Configuration graphique de la fenètre
Config.set('graphics', 'height', '500')


jeu = jeuApp()
jeu.run()