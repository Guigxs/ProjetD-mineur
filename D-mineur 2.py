#LIBRAIRIES KIVY

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

#AUTRES LIBRAIRIES

import time
import random
import sys

###############################################################################

class JeuDemineurApp(App): #Classe principale contenant les info sur le jeu 
    def build(self):
        colonne = 10
        ligne = 10
        mine = 11
        niveau = 1

        globalBoxLayout = MyBoxLayout()
        grille = MyGridLayout(ligne, colonne, mine, niveau) #Renvoi à la GridLayout le nombre de colonnes, lignes et mines

        globalBoxLayout.add_widget(grille)
        
        return globalBoxLayout


class OnPressButton(Button): #Boutton pressé de la grille
    pass


class MyBoxLayout(BoxLayout): #Box principale (contenant top et grille)
    pass


class MyGridLayout(GridLayout): #Grille de : 'self.ligne' ligne et 'self.colonne' colonnes avec 'self.mine' mines
    def __init__(self, ligne, colonne, mine, niveau):
        super(MyGridLayout, self).__init__()
        self.ligne = ligne
        self.colonne = colonne
        self.mine = mine
        self.choix_places = list()
        self.niveau = niveau
        
        with open ("data.txt", "w") as file: #Ecrit les ref (references de chaque bouton) et leur place dans un fichier
            self.total = []

            for i in range(self.ligne): #Genere les 'self.ligne' lignes
                self.line = []

                for j in range(self.colonne): #Genere les 'self.colonne' colonnes
                    case = MyButton(ref = [j, i], id = '[{}, {}]'.format(j, i))
                    case.bind(on_release=self.check)
                    self.add_widget(case)
                    self.line.append(case.ref) #Ajout des réferences de chaque bouton a une liste

                self.total.append(self.line) #Ajout de la sous-liste contenant les réferences à une autre liste

            file.write(str(self.total)) #Ecrit dans le fichier data.txt

        self.random() #Appel de la méthode random qui génere des position de mine aléatoires


    def random(self): #Methode random choisi N(self.mine) bombes aux positions(self.paires)
        self.choix_places = []
        with open("bombes.txt", "w") as file:
            for a in range(self.mine):
                self.paires = []
                for b in range(2): #choix de 2 valeurs correspondant aux (x, y) de la mine
                    self.paires.append(random.randrange(self.colonne))

                self.choix_places.append(self.paires) #Ajout de la liste des emplacements dans un liste contenant les N emplacements des bombes

            print("Les", self.mine,"mines se situent aux emplacements suivants : ", self.choix_places) #affichage des N mines (x, y) à la console
            file.write(str(self.choix_places)) #Ecriture des emplacements des bombes dans le fichier bombes.txt

    def check(self, source): #Methode check verrifie si on est sur une bombe ou combien aux alentours
        for i in self.choix_places: #Boucle qui check si on est sur une bombes
            if source.id == str(i):
                FirstPopup(self.mine, self.niveau).open() #Si oui : Ouvre la popup1
            else:
                source.background_normal = OnPressButton().background_normal #Si non rend le bouton gris

        bombes = 0
        for k in self.choix_places: #Boucle qui check combien de bombe il y a autour
            for l in range(-1, 2): #Boucle pour faire le carré autour de la position
                for m in range(-1, 2): #Boucle pour faire le carré autour de la position
                    if k == [source.ref[0]+l, source.ref[1]+m]: 
                        bombes+=1 #Ajout de la bombe
        
        if bombes>0: #Affiche le nombre de bombe si il y en a autour
            source.text = str(bombes)                    
        print(bombes) #Affiche le nombre de bombe a la console


class FirstPopup(Popup): #Popup qui demande : quitter ou sauvegarder 
    def __init__(self, mine, niveau):
        super(FirstPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau

    def openSecondPopup(self): #Ouvertue de la 2eme popup 
        SecondPopup(self.mine, self.niveau).open()
        self.dismiss() #Quitte la popup

    def quit(self): #Quitter le jeu
        JeuDemineurApp().stop()


class SecondPopup(Popup): #Popup qui enregistre le pseudo puis qui quitte
    def __init__(self, mine, niveau):
        super(SecondPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau

    def save(self): #Quand on clique sur sauvgarder
        nom = self.pseudo.text #Recupere le pseudo
        mine = self.mine #Recupere les points
        niveau = self.niveau
        self.temps = "**TEMPS**" #Recupere le temps
        with open('scores.txt', 'a') as file: #Ouvre le ficher pour y enregistrer les scores avec les pseudo
            file.write("--------------------\nPseudo : {}\nMines : {} (Niveau : {})\nTemps : {}\nDate : {}\n".format(nom, mine, niveau, self.temps, str(time.asctime()))) #Affichage dans fichier
        time.sleep(1) #Attend 1seconde
        FirstPopup.quit(self)


class MyButton(Button): #Widget boutton pour la grille
    def __init__(self, ref, id):
        super(MyButton, self).__init__()
        self.ref = ref
        self.id = id
        self.background_normal


jeu = JeuDemineurApp()
jeu.run()
