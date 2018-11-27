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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

Config.set('input', 'mouse', 'mouse,disable_multitouch')

#AUTRES LIBRAIRIES

import time
import random
import sys


############################################ AUTRES CLASSE ########################################################


class MyClock(Label): #Label qui compte le temps
    def up(self, *args):
        self.text = "Temps : {} sec".format(str(int(time.clock()))) #Le text du label contient le temps chaque sec



class Jeu2App(App): #App qui lance le jeu
    def build(self):

        self.title = "Démineur" #Titre de la page
        self.icon = "images/icon.png" #Icon de la page

        manager = Manager()

        return manager


##################################################### ECRANS ######################################################


class Manager(ScreenManager):
    screen_launcher = ObjectProperty(None)
    screen_easy = ObjectProperty(None)
    screen_medium = ObjectProperty(None)
    screen_hard = ObjectProperty(None)


class Launcher(Screen):
    pass


class Easy(Screen):
    def on_enter(self, **kw):
        super().__init__(**kw)

        self.add_widget(MyGlobalBoxLayout(10, 10, 11, 1))



class Medium(Screen):
    def on_enter(self, **kw):
        super().__init__(**kw)
    
        self.add_widget(MyGlobalBoxLayout(15, 15, 23, 2))



class Hard(Screen):
    def on_enter(self, **kw):
        super().__init__(**kw)
    
        self.add_widget(MyGlobalBoxLayout(20, 20, 60, 3))



###################################################### LAYOUTS ####################################################


class MyTopBoxLayout(BoxLayout): #BoxLayout partie supperieure
    pass


class MyBoxLayout(BoxLayout): #BoxLayout contenant la grille et parite suppérieure
    pass


class MyGlobalBoxLayout(BoxLayout): #BoxLayout contenant MyBoxLayout
    def __init__(self, ligne, colonne, mine, niveau):
        super(MyGlobalBoxLayout, self).__init__()

        self.ligne = ligne
        self.colonne = colonne
        self.mine = mine
        self.niveau = niveau


        myClock = MyClock() 
        Clock.schedule_interval(myClock.up, 1) #Update time chaque sec

        top = MyTopBoxLayout()
        grille = MyGridLayout(self.ligne, self.colonne, self.mine, self.niveau) #Appel GridLayout en f du niveau
        box = MyBoxLayout()

        top.add_widget(myClock)
        box.add_widget(top) #Imbrications
        box.add_widget(grille)

        self.add_widget(box) #Ajout a la Box


class MyGridLayout(GridLayout): #Grille de : 'self.ligne' ligne et 'self.colonne' colonnes avec 'self.mine' mines
    def __init__(self, ligne, colonne, mine, niveau):
        super(MyGridLayout, self).__init__()
        self.rows = ligne
        self.cols = colonne
        self.mine = mine
        self.choix_places = list()
        self.niveau = niveau
        self.drapeau = self.mine

   
        with open ("data.txt", "w") as file: #Ecrit les ref (references de chaque bouton) et leur place dans un fichier
            self.total = []

            for i in range(self.rows): #Genere les 'self.roxs' lignes
                self.line = []

                for j in range(self.cols): #Genere les 'self.cols' colonnes
                    case = MyButton(ref = [j, i], id = '[{}, {}]'.format(j, i), state = 'normal')
                    case.bind(on_touch_up=self.check) #Appel check quand on relache
                    case.bind(on_touch_up=self.asdrapeau) #Appel drapeau quand on clic
                    self.add_widget(case)
                    self.line.append(case) #Ajout des réferences de chaque bouton a une liste

                self.total.append(self.line) #Ajout de la sous-liste contenant les réferences à une autre liste

            file.write(str(self.total)) #Ecrit dans le fichier data.txt

        self.random() #Appel de la méthode random qui génere des position de mine aléatoires


    def random(self): #Methode random choisi N(self.mine) bombes aux positions(self.paires)
        self.choix_places = []
        with open("bombes.txt", "w") as file:
            for a in range(self.mine):
                self.paires = []
                for b in range(2): #choix de 2 valeurs correspondant aux (x, y) de la mine
                    self.paires.append(random.randrange(self.cols))

                self.choix_places.append(self.paires) #Ajout de la liste des emplacements dans un liste contenant les N emplacements des bombes

            print("Les", self.mine,"mines se situent aux emplacements suivants : ", self.choix_places) #affichage des N mines (x, y) à la console
            file.write(str(self.choix_places)) #Ecriture des emplacements des bombes dans le fichier bombes.txt

    def check(self, source, touch): #Methode check verrifie si on est sur une bombe ou combien aux alentours
        if touch.button == 'left' and touch.grab_current != None:
        
            bombes = 0
            for i in self.choix_places: #Boucle qui check si on est sur une bombes
                if source.id == str(i):
                    source.background_normal = ''
                    source.text = "BOOM"
                    source.background_color = (0, 0, 0, 1)
                    FirstPopup(self.mine, self.niveau).open() #Si oui : Ouvre la popup1
                
                    bombe = 0

                else:
                    source.background_normal = OnPressButton().background_down #Si non rend le bouton gris
                    source.state = 'down'

                    for l in range(-1, 2): #Boucle pour faire le carré autour de la position
                        for m in range(-1, 2): #Boucle pour faire le carré autour de la position
                            if i == [source.ref[0]+l, source.ref[1]+m]: 
                                bombes+=1 #Ajout de la bombe

                                
                                
                                #Si pas de bombes alors on met les cases en gris


                    if bombes>0: #Affiche le nombre de bombe si il y en a autour
                        source.text = str(bombes)  
                    
            #if bombes == 0:
                #for l in range(-1, 2): #Boucle pour faire le carré autour de la position
                    #for m in range(-1, 2): #Boucle pour faire le carré autour de la position
                        #but = self.total[source.ref[1]+l][source.ref[0]+m] 
                        #but.background_normal = 'images/gris.png'
                            


    def asdrapeau(self, source, touch): #Affiche les drapeaux
        if touch.button == 'right' and touch.grab_current != None:
            print("right")
            source.background_normal = "images/drapeau.png"
            print(source)



class MyButton(Button): #Widget boutton pour la grille
    def __init__(self, ref, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.ref = ref

class OnPressButton(Button): #Boutton pressé de la grille
    pass


################################################# POPUPS ##########################################################


class FirstPopup(Popup): #Popup qui demande : quitter ou sauvegarder 
    def __init__(self, mine, niveau):
        super(FirstPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau

    def openSecondPopup(self): #Ouvertue de la 2eme popup 
        SecondPopup(self.mine, self.niveau).open()
        self.dismiss() #Quitte la popup

    def quit(self): #Quitter le jeu
        Jeu2App().stop()


class SecondPopup(Popup): #Popup qui enregistre le pseudo puis qui quitte
    def __init__(self, mine, niveau):
        super(SecondPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau

    def save(self): #Quand on clique sur sauvgarder
        nom = self.pseudo.text.lstrip().rstrip() #Recupere le pseudo
        mine = self.mine #Recupere les points
        niveau = self.niveau
        self.temps = 0#MyClock().text #Recupere le temps

        if nom != "" :
            with open('scores.txt', 'a') as file: #Ouvre le ficher pour y enregistrer les scores avec les pseudo
                file.write("--------------------\nPseudo : {}\nMines : {} (Niveau : {})\nTemps : {}\nDate : {}\n".format(nom, mine, niveau, self.temps, str(time.asctime()))) #Affichage dans fichier
            time.sleep(1) #Attend 1seconde
            FirstPopup.quit(self)


Jeu2App().run()