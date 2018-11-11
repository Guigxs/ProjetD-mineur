#----------------------------------------------------LIBRAIRIES KIVY


from kivy.app import App                           
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock


#-----------------------------------------------------AUTRES LIBRAIRIES 


from kivy.config import Config                         
import time
import random
import sys


class jeuApp(App):

    def build (self):

        self.title = "Démineur" #titre
        self.icon = "images/icon.png" #image


#----------------------initialisation des variables----------------------


        self.ligne = 16 #Nombre de lignes pour le jeu                            
        self.colonne = 16 #Nombre de colonnes pour le jeu

        self.level = 28 #Niveau de difficulté du jeu (nombre de bombes)

        self.Lligne=[] #Sous-liste contenant les nom des boutons pour une ligne
        self.Ltotale=[] #Liste contenant les sous-liste de boutons 

        self.drapeau = 28 #Nombre de drapeaux disponibles

        self.paires = [] #Liste de 2 elements contenant des (x, y) au hasard
        self.choix_places = [] #Liste de la liste contenant les emplacements des bombes


#-------------------Choix aléatoire---------------

        for a in range(self.level):
            self.paires = []
            for b in range(2): #choix de 2 valeurs correspondant aux (x, y) de la mine
                self.paires.append(random.randrange(16))

            self.choix_places.append(self.paires) #Ajout de la liste des emplacements dans un liste contenant les 28 emplacements des bombes

        print("Les mines se situent aux emplacements suivants : ", self.choix_places) #affichage des mines (x, y) à la console


#----------------Boxes haut----------------------


        box = BoxLayout(orientation = 'vertical', size_hint=(None, None), size = (400, 500)) #Boxe generale


        top_box = BoxLayout(orientation='horizontal', size_hint=(1, .1)) #Partie du dessus (top)

        
        
        time_box = AnchorLayout(anchor_x='left', anchor_y='top') #Definition de l'emplacement
        time_box.add_widget(Label(text = "Time played : {}".format("0"), size_hint=(1, 1))) #Ajout des propriétés d'affichage
        top_box.add_widget(time_box) # Ajout du temps à la sous-boxe

        
        restart_box = AnchorLayout(anchor_x='center', anchor_y='top') #Definition de l'emplacement
        self.restart_button = Button(text = "Restart", size_hint=(1, 1))#Ajout des propriétés d'affichage
        self.restart_button.bind(on_release=self._restart) #Renvoi la methode _restart quand on clic
        restart_box.add_widget(self.restart_button)
        top_box.add_widget(restart_box) # Ajout du boutton restart à la sous-boxe


        points_box = AnchorLayout(anchor_x='right', anchor_y='top') #Definition de l'emplacement
        self.counting_points = Label(text = "Flags : 28", size_hint=(1, 1)) #Ajout des propriétés d'affichage
        points_box.add_widget(self.counting_points)
        top_box.add_widget(points_box) # Ajout des points à la sous-boxe

        box.add_widget(top_box) #Ajout de toutes les sous boxe à la top_box


#------------------ Grille ----------------------
            

        bottom_box = GridLayout(rows = self.ligne, cols = self.colonne) #Partie du dessous (bottom)
        with open("data.txt", "w") as file: #Ouverture du fichier pour y ecrire les noms des boutons (Pas utile pour le moment)

            for self.i in range(self.ligne): #On repete l'action pour chaque lignes          
                for self.e in range(self.colonne): #On répete l'action pour chaque colonnes
                    self.grid_button = Button(background_down = "images/gris.png") #Quand on enfonce le bouton 
                    self.grid_button.bind(on_release=self._grid_affichage) #Appel la méthode pour réveler la case
                    self.grid_button.bind(on_press=self._drapeau) #Appel la methode pour afficher les drapeaux et compter les points
                    self.grid_button.bind(on_release=self._compare) #Appel la methode pour verifier si on est pas sur une bombe
                    bottom_box.add_widget(self.grid_button)
                    self.Lligne.append(str(self.grid_button)) #ajout du chiffre du nom du bouton dans la sous-liste Lligne

                self.Ltotale.append(self.Lligne) #Ajoute la sous-liste dans la liste Ltotale
                self.Lligne =[] #Remise à 0 de l'ensemble Lligne pour recommencer avec la colonne suivante


            file.write(str(self.Ltotale)) #Ecrit le dico_global dans data.txt


        box.add_widget(bottom_box) #Ajout de la sous-box bottom_box à la box
        return box #Revoi la box


#------------- Boucles évenementielles -------------------------


    def _timer (self): #Chronometre
        pass

    def _restart (self, other): #Opération boutton restart    
        pass

    def _drapeau (self, source): #Affichage des drapeaux et des points
        source.background_normal = "images/drapeau.png" #Change le background en drapeau 
        self.drapeau -= 1 #Change les points (Départ de 28 -> 0)
        self.counting_points.text = "Flags : " + str(self.drapeau) #Affichage des points au fur et a mesure


    def _grid_affichage(self, source): #Affichage des cases quand on clique
        source.background_normal = "images/gris.png" #Chagement du background quand clic


    def _compare(self, source): #Test si on clique sur une bombe
        for t in self.choix_places: #Création d'une boucle pour vérifier si on est sur une mine
            if str(source) == self.Ltotale[t[1]][t[0]]: #Comparaison de l'emplacment du bouton avec l'emplacment de la mine (x, y)
                sys.exit(0) #Quitte si condition remplie


#-------------------------Fin de la class----------------------------


Config.set('graphics', 'width', '400') #Configuration graphique de la fenètre (largeur)
Config.set('graphics', 'height', '500') #Configuration graphique de la fenètre (hauteur)


jeu = jeuApp() 
jeu.run() #Lancement du jeu