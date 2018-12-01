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
    
        self.add_widget(MyGlobalBoxLayout(15, 15, 28, 2))



class Hard(Screen):
    def on_enter(self, **kw):
        super().__init__(**kw)
    
        self.add_widget(MyGlobalBoxLayout(20, 20, 60, 3))



###################################################### LAYOUTS ####################################################


class MyTopBoxLayout(BoxLayout): #BoxLayout partie supperieure

    flagLabel = ObjectProperty()
    timeLabel = ObjectProperty()

    def __init__(self, drapeau, **kwargs):
        super(MyTopBoxLayout, self).__init__(**kwargs)
        self.counter = 0
        Clock.schedule_interval(self.callback, 1)
        self.drapeau = drapeau
        self.flagLabel.text = str("{} mines à trouver".format(self.drapeau))

    def callback(self, dt):
        if self.counter < 1000:
            self.counter += 1
            self.timeLabel.text = str("Temps: {} sec".format(self.counter))
            global temps 
            temps = self.counter
        else:
            sys.exit(0)

    def restart(self):
        sys.exit(0)
    

class MyBoxLayout(BoxLayout): #BoxLayout contenant la grille et parite suppérieure
    pass


class MyGlobalBoxLayout(BoxLayout): #BoxLayout contenant MyBoxLayout
    def __init__(self, ligne, colonne, mine, niveau):
        super(MyGlobalBoxLayout, self).__init__()

        self.ligne = ligne
        self.colonne = colonne
        self.mine = mine
        self.niveau = niveau


        top = MyTopBoxLayout(self.mine)
        grille = MyGridLayout(self.ligne, self.colonne, self.mine, self.niveau) #Appel GridLayout en f du niveau
        box = MyBoxLayout()

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
        self.list_drapeau = []
        self.bon_drapeau = 0


   
        with open ("data.txt", "w") as file: #Ecrit les ref (references de chaque bouton) et leur place dans un fichier
            self.total = []

            for i in range(self.rows): #Genere les 'self.roxs' lignes
                self.line = []

                for j in range(self.cols): #Genere les 'self.cols' colonnes
                    case = MyButton(ref = [j, i], state = 'normal')
                    case.bind(on_touch_up=self.check) #Appel check quand on relache
                    case.bind(on_touch_up=self.hasdrapeau) #Appel drapeau quand on clic
                    self.add_widget(case)
                    self.line.append(case) #Ajout des réferences de chaque bouton a une liste

                self.total.append(self.line) #Ajout de la sous-liste contenant les réferences à une autre liste

            file.write(str(self.total)) #Ecrit dans le fichier data.txt

        self.random() #Appel de la méthode random qui génere des position de mine aléatoires


    def randompaires(self):
        self.paires = []
        for b in range(2): #choix de 2 valeurs correspondant aux (x, y) de la mine
            self.paires.append(random.randrange(self.cols))
        
        return self.paires


    def random(self): #Methode random choisi N(self.mine) bombes aux positions(self.paires)
        self.choix_places = []
        with open("bombes.txt", "w") as file:
            for a in range(self.mine):
                self.randompaires()

                if self.paires in self.choix_places:
                    print('Doublons en :', self.paires)
                    self.paires = self.randompaires()
                    print ('Nouvelle paires : ', self.paires)
                    
                
                self.choix_places.append(self.paires) #Ajout de la liste des emplacements dans un liste contenant les N emplacements des bombes
                

            print("Les", self.mine,"mines se situent aux emplacements suivants : ", self.choix_places) #affichage des N mines (x, y) à la console
            file.write(str(self.choix_places)) #Ecriture des emplacements des bombes dans le fichier bombes.txt


    def hasdied(self, source):
        print("Mort ou vivant?")
        self.bombes = 0
        for i in self.choix_places: #Boucle qui check si on est sur une bombes
            if source.ref == i:
                source.background_normal = ''
                source.text = "BOOM"
                source.background_color = (0, 0, 0, 1)
                self.bombes = -1
                self.checkdrap()
                FirstPopup(self.mine, self.niveau, self.bon_drapeau).open() #Si oui : Ouvre la popup1


    def hasbombesaround(self, source):
        self.bombes=0
        print("\nChecking around:", source.ref)
        for i in self.choix_places:
            for l in range(-1, 2): #Boucle pour faire le carré autour de la position
                for m in range(-1, 2): #Boucle pour faire le carré autour de la position
                    if i == [source.ref[0]+l, source.ref[1]+m]: #Si la case autour de la source est une mine on l'ajoute à self.mine
                        print('Bombe en:', i)
                        self.bombes+=1 #Ajout de la bombe
                        source.text = 'Bombe'
                        
        source.id = 'Checké'                   
        

    def hasbombesaroundcase(self, source):

        print('\n-- Cherche en profondeur autour de la case :', source.ref, '--')
        for n in range(-1, 2): #Boucle pour faire le carré autour de la position
            for o in range(-1, 2): #Boucle pour faire le carré autour de la position
                    if 0 <= (source.ref[0]+n) and (source.ref[0]+n) < self.cols and 0 <= (source.ref[1]+o) and (source.ref[1]+o) < self.rows: #Verifie que on est pas hors zone
                        actualButton = self.total[source.ref[1]+o][source.ref[0]+n] # On créé un nouveau bouton autour de la source

                        if actualButton.id != 'Checké':
                            self.hasbombesaround(actualButton) #On lance le check autour du boutton
                            actualButton.background_normal = OnPressButton().background_down #On rend le bouton gris
                            
                            print('Relativement en:', [n, o])

                            if self.bombes > 0:
                                print("Ecriture:", self.bombes, "sur la case")
                                actualButton.text = str(self.bombes)

                            else:
                                print("Pas de bombes!")
                                self.hasbombesaroundcase(actualButton)

                    else:
                        print("Impossible : en dehors de la zone") 
                    

    def check(self, source, touch): #Methode check verrifie si on est sur une bombe ou combien aux alentours
        if touch.button == 'left' and touch.grab_current != None:
            print('\n-------------- Start checking... ----------------\n')
            print('Ref :', source.ref)

            self.hasdied(source)

            if self.bombes >=0:
                print('Vivant!')
                source.background_normal = OnPressButton().background_down #On rend le bouton gris

                self.hasbombesaround(source) #Check si bombes autour de la source

                if self.bombes > 0: #Si il y  a des bombes autour de la source on l'ecrit dessus
                    print("Ecriture:", self.bombes)
                    source.text = str(self.bombes)

                else: #Sinon on ecrit "Pas de bombe" et on cherche autour de autour de la source
                    print("\nPas de bombes, recherche en profondeur...")
                    self.hasbombesaroundcase(source)

            else:
                print("MORT!!")
            
            print('\n----------------- Fin du check -------------------\n')


    def hasdrapeau(self, source, touch): #Affiche les drapeaux
        
        if touch.button == 'right' and touch.grab_current != None: #Si on fait un clic droit
            self.bon_drapeau = 0
            if source.ref in self.list_drapeau: #Si le drapeau est deja dans la liste des potentielles bombes
                print('\n-- Suppression du drapeau en:', source.ref, '--')
                source.background_normal = "atlas://data/images/defaulttheme/button" #On remet le fond en normal
                self.list_drapeau.remove(source.ref) #On le supprime
                self.drapeau +=1 #On ajoute 1 aux nombres de drapeaux restants a trouver

                print('Nombre de drapeaux restant:', self.drapeau, 'en', self.list_drapeau, '\n')

            else: #Si la liste de drapeau ne contient pas celui qu'on veut mettre
                if self.drapeau >= 1: #Et si il reste des drapeaux a mettre
                    print('\n-- Nouveau drapeau en:', source.ref, '--')
                    self.list_drapeau.append(source.ref) #On ajoute le potentiel drapeau a une liste 
                    self.drapeau -= 1 #On retire 1 au nombres de drapeaux restants
                    source.background_normal = "images/drapeau.png" #On met le fond en drapeau

                    print('Nombre de drapeaux restant:', self.drapeau, 'en', self.list_drapeau, '\n')

                if self.drapeau == 0:
                    self.checkdrap()     
                
            if self.bon_drapeau == len(self.choix_places):
                WinPopup(self.mine, self.niveau, self.bon_drapeau).open()
                print("WIN!!!")


    def checkdrap(self):
        print("Debut du check des drapeaux...")
        for bombe in self.choix_places:
            for drap in self.list_drapeau:
                if drap == bombe:
                    self.bon_drapeau += 1

        print("Bons drapeaux :", self.bon_drapeau)


class MyButton(Button): #Widget boutton pour la grille
    def __init__(self, ref, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.ref = ref

class OnPressButton(Button): #Boutton pressé de la grille
    pass


################################################# POPUPS ##########################################################


class FirstPopup(Popup): #Popup qui demande : quitter ou sauvegarder 
    def __init__(self, mine, niveau, drapeau):
        super(FirstPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau
        self.drapeau = drapeau

    def openSecondPopup(self): #Ouvertue de la 2eme popup 
        SecondPopup(self.mine, self.niveau, 'Perdu', self.drapeau).open()
        self.dismiss() #Quitte la popup

    def quit(self): #Quitter le jeu
        Jeu2App().stop()


class WinPopup(Popup):
    def __init__(self, mine, niveau, drapeau):
        super(WinPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau
        self.drapeau = drapeau

    def openSecondPopup(self): #Ouvertue de la 2eme popup 
        SecondPopup(self.mine, self.niveau, 'Gagne', self.drapeau).open()
        self.dismiss() #Quitte la popup

    def quit(self): #Quitter le jeu
        Jeu2App().stop()


class SecondPopup(Popup): #Popup qui enregistre le pseudo puis qui quitte
    def __init__(self, mine, niveau, etat, drapeau):
        super(SecondPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau
        self.etat = etat
        self.drapeau = drapeau
        self.temps = temps
        self.score = 4

    def save(self): #Quand on clique sur sauvgarder
        nom = self.pseudo.text.lstrip().rstrip() #Recupere le pseudo
        if nom != "" :
            with open('scores.txt', 'a') as file: #Ouvre le ficher pour y enregistrer les scores avec les pseudo
                file.write("--------------------\nPseudo : {}\n[{} avec {} bon(s) drapeau(x)]\nScore : {}\nMines : {} (Niveau : {})\nTemps : {} sec\nDate : {}\n".format(nom, self.etat, self.drapeau, self.score, self.mine, self.niveau, self.temps, str(time.asctime()))) #Affichage dans fichier
            time.sleep(1) #Attend 1seconde
            FirstPopup.quit(self)


Jeu2App().run()