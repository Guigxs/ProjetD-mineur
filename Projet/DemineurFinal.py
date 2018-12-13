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
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

Config.set('input', 'mouse', 'mouse,disable_multitouch')

#AUTRES LIBRAIRIES

import time
import random
import sys
import json


############################################ AUTRES CLASSE ########################################################


class JeuApp(App): #App qui lance le jeu
    def build(self):

        self.title = "Démineur" #Titre de la page
        self.icon = "images/icon.png" #Icon de la page


        Window.set_system_cursor('hand')
        Window.size = (800, 696)
        Window.left = 290
        Window.top = 31


        manager = Manager()
        return manager


##################################################### ECRANS ######################################################


class Manager(ScreenManager):
    first_screen = ObjectProperty(None)
    screen_easy = ObjectProperty(None)
    screen_medium = ObjectProperty(None)
    screen_hard = ObjectProperty(None)


class FirstScreen(Screen):
    pass


class Easy(Screen):
    def on_pre_enter(self, **kw):
        super().__init__(**kw)
        
        self.add_widget(MyGlobalBoxLayout(8, 8, 9, 1))


class Medium(Screen):
    def on_pre_enter(self, **kw):
        super().__init__(**kw)

        self.add_widget(MyGlobalBoxLayout(10, 10, 15, 2))


class Hard(Screen):
    def on_pre_enter(self, **kw):
        super().__init__(**kw)
    
        self.add_widget(MyGlobalBoxLayout(15, 15, 30, 3))



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
        self.bombes = 0
        for i in self.choix_places: #Boucle qui check si on est sur une bombes
            if source.ref == i:
                source.background_normal = ''
                source.text = "BOOM"
                source.background_color = (0, 0, 0, 1)
                self.bombes = -1 #Pour pas entrer dans les boucles suivantes
                self.checkdrap() #Lance le check des drapeaux pour avoir un score
                self.checkCaseRev() #Appel de la methode pour compter le nombre de case découverte
                FirstPopup(self.mine, self.niveau, self.bon_drapeau, self.score).open() #Si oui : Perdu, ouvre popup
                print("Perdu, ouverture de la popup...")


    def hasbombesaround(self, source):
        self.bombes=0
        for i in self.choix_places:
            for l in range(-1, 2): #Boucle pour faire le carré autour de la position
                for m in range(-1, 2): #Boucle pour faire le carré autour de la position
                    if i == [source.ref[0]+l, source.ref[1]+m]: #Si la case autour de la source est une mine on l'ajoute à self.mine
                        self.bombes+=1 #Ajout de la bombe
                        
        source.id = 'Checké'    #Rend la case "checké" pour la récursivité               
        

    def hasbombesaroundcase(self, source): #Methode récursive
        for n in range(-1, 2): #Boucle pour faire le carré autour de la position
            for o in range(-1, 2): #Boucle pour faire le carré autour de la position
                    if 0 <= (source.ref[0]+n) and (source.ref[0]+n) < self.cols and 0 <= (source.ref[1]+o) and (source.ref[1]+o) < self.rows: #Verifie que on est pas hors zone
                        actualButton = self.total[source.ref[1]+o][source.ref[0]+n] # On créé un nouveau bouton autour de la source

                        if actualButton.id != 'Checké':
                            self.hasbombesaround(actualButton) #On lance le check autour du boutton
                            actualButton.background_normal = OnPressButton().background_down #On rend le bouton gris
                            

                            if self.bombes > 0: #Apres le check autour on ecrit dessus si y a des bombes
                                actualButton.text = str(self.bombes)

                            else: #Sinon on appel la meme fonction avec le "nouveau bouton" --> RECURSION
                                self.hasbombesaroundcase(actualButton)
                    

    def check(self, source, touch): #Methode check verrifie si on est sur une bombe ou combien aux alentours
        if touch.button == 'left' and touch.grab_current != None:
            self.hasdied(source) #Regarde si je suis en vie

            if self.bombes >=0:

                source.background_normal = OnPressButton().background_down #On rend le bouton gris quand on presse 

                self.hasbombesaround(source) #Check si bombes autour de la source

                if self.bombes > 0: #Si il y  a des bombes autour de la source on l'ecrit dessus et on sort de la condition
                    source.text = str(self.bombes)

                else: #Sinon on cherche "autour de autour" de la source
                    self.hasbombesaroundcase(source)


    def hasdrapeau(self, source, touch): #Affiche les drapeaux
        if touch.button == 'right' and touch.grab_current != None: #Si on fait un clic droit
            self.bon_drapeau = 0
            if source.ref in self.list_drapeau: #Si le drapeau est deja dans la liste des drapeaux
                print('\n-- Suppression du drapeau en:', source.ref, '--')
                source.background_normal = "atlas://data/images/defaulttheme/button" #On remet le fond en normal
                self.list_drapeau.remove(source.ref) #On le supprime
                self.drapeau +=1 #On ajoute 1 aux nombres de drapeaux restants a trouver

                print('Nombre de drapeaux restant:', self.drapeau, '\nLes drapeaux sont:', self.list_drapeau, '\n')

            else: #Si la liste de drapeau ne contient pas celui qu'on veut mettre
                if self.drapeau >= 1: #Et si il reste des drapeaux a mettre
                    print('\n-- Nouveau drapeau en:', source.ref, '--')
                    self.list_drapeau.append(source.ref) #On ajoute le potentiel drapeau a une liste 
                    self.drapeau -= 1 #On retire 1 au nombres de drapeaux restants
                    source.background_normal = "images/drapeau.png" #On met le fond en drapeau

                    print('Nombre de drapeaux restant:', self.drapeau, '\nLes drapeaux sont:', self.list_drapeau, '\n')

                if self.drapeau == 0: #Quand il n'y a plus de drapeau à mettre on appel la methode pour checker si ils sont bons
                    self.checkdrap()     
                
            if self.bon_drapeau == len(self.choix_places): #Si les drapeaux sont bons, on lance le gain
                for i in self.total:
                    for j in i:
                        if j.background_normal == 'atlas://data/images/defaulttheme/button': #On revele toutes les case en cas de gain pour avoir un score max
                            j.background_normal = 'images/gris.png'

                self.checkCaseRev() #Appel de la methode pour compter le nombre de case découverte
                WinPopup(self.mine, self.niveau, self.bon_drapeau, self.score).open() #Lance la popup de gain
                print("Gagné, ouverture de la popup...")


    def checkdrap(self): #Méthode qui "scan" tout les drapeaux et qui regarde combien on en a de bons
        print("Debut du check des drapeaux...")
        for bombe in self.choix_places:
            for drap in self.list_drapeau:
                if drap == bombe:
                    self.bon_drapeau += 1 #Renvoi le nombre de bons drapeaux


    def checkCaseRev(self):
        self.caseRev = 0
        for i in self.total:
            for j in i:
                if j.background_normal == 'images/gris.png':
                    self.caseRev += 1
        
        print('Case revelee: ' + str(self.caseRev))

        self.compute() #Appel la methode qui calcule le score


    def compute(self):
        const = (self.cols*self.rows) - self.mine #Formule dans les consignes
        self.score = int(100*(self.caseRev/const))


class MyButton(Button): #Widget boutton pour la grille
    def __init__(self, ref, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.ref = ref

class OnPressButton(Button): #Boutton pressé de la grille
    pass


################################################# POPUPS ##########################################################


class FirstPopup(Popup): #Popup qui demande : quitter ou sauvegarder 
    def __init__(self, mine, niveau, drapeau, score):
        super(FirstPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau
        self.drapeau = drapeau
        self.score = score

        self.son()

    def son(self):
        sound = SoundLoader.load('images/12420.wav')
        sound.play()
        for i in range(50):
            Window.top = random.randint(35, 40)
            Window.left = random.randint(295, 300)
            time.sleep(.05)

    def openSecondPopup(self): #Ouvertue de la 2eme popup 
        SecondPopup(self.mine, self.niveau, 'Perdu', self.drapeau, self.score).open()
        self.dismiss() #Quitte la popup

    def quit(self): #Quitter le jeu
        JeuApp().stop()


class WinPopup(Popup):
    def __init__(self, mine, niveau, drapeau, score):
        super(WinPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau
        self.drapeau = drapeau
        self.score = score

        self.son()
    
    def son(self):
        sound = SoundLoader.load('images/level-up.wav')
        sound.play()
        sleep = 0.2

        Window.left = 0
        time.sleep(sleep)
    
        Window.left = 600
        time.sleep(sleep)

        Window.left = 290
        time.sleep(sleep)
        

    def openSecondPopup(self): #Ouvertue de la 2eme popup 
        SecondPopup(self.mine, self.niveau, 'Gagné', self.drapeau, self.score).open()
        self.dismiss() #Quitte la popup

    def quit(self): #Quitter le jeu
        JeuApp().stop()


class SecondPopup(Popup): #Popup qui enregistre le pseudo puis qui quitte
    def __init__(self, mine, niveau, etat, drapeau, score):
        super(SecondPopup, self).__init__()
        self.mine = mine
        self.niveau = niveau
        self.etat = etat
        self.drapeau = drapeau
        self.temps = temps
        self.score = score
        self.date = time.asctime()

    def save(self): #Quand on clique sur sauvgarder
        nom = self.pseudo.text.lstrip().rstrip() #Recupere le pseudo en nettoyant le str à gauche et a droite

        if nom != "" : #Si pas de pseudo, ne fait rien, si oui on continue
            print("Score :", str(self.score))

            try :
                with open('scores.json', 'r', encoding="utf-8")as file: #On essaye d'ouvrir le fichier json
                    data = file.read() #On recupere ce qu'il y a dedans 

                    if data != "":
                        self.data2 = json.loads(data) #Si il y a quelque chose d'écrit dedans on le récupere 
                    
                    else:
                        self.data2 = {"Content": []} #Sinon on ecrit
            except:
                print("Ficher json non-existant ! Création d'un nouveau ficher: scores.json...") #Si il existe pas ou pas conforme, on le créé/modifie aux normes
                with open('scores.json', 'w', encoding="utf-8")as file:
                    self.data2 = {"Content": []}


            with open('scores.json', 'w', encoding="utf-8")as file: #On prepare le fichier pour ecrire dedans
                
                score = {"Nom":nom, "Etat":self.etat, "Score": self.score, "Temps":self.temps, "Niveau":self.niveau, "Drapeaux trouves":self.drapeau, "Date":self.date} #Ce qu'on va y ecrire
                
                self.data2["Content"].append(score) #Ajoute du contenu à la liste globale


                ready = json.dumps(self.data2, indent =4) #Ontransfomre le ficher en json
                file.write(ready) #On l'écrit


            self.dismiss() #Quitte la popup
            ScoresPopup().open() #Ouvre la popup des scores


class ScoresPopup(Popup):
    total_boxlayout = ObjectProperty() #Lien avec le fichier kv
    global_boxlayout = ObjectProperty()
    top_boxlayout = ObjectProperty()
    list_boxlayout = ObjectProperty()
    max_boxlayout = ObjectProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        with open("scores.json", 'r', encoding="utf-8") as file: #On ouvre le ficher pour afficher les scores
            contenu = file.read()
            trans = json.loads(contenu) #On transforme le ficher et on recupere la liste 

            if len(trans["Content"]) >= 2: #Condition qui cherche le HIGH SCORE si il y a au moins un score dedans, sinin non
                self.a = trans['Content'][0]
            
                for i in range(len(trans['Content'])): #Cherche pour chaque score

                    if self.a["Score"] < trans['Content'][i]['Score']: #Renvoie le score le plus haut
                        self.a = trans['Content'][i]
                
                self.max_boxlayout.add_widget(Label(text = 'HIGH SCORE', color = (1, 0, 0, 1))) #Ecrit en rouge le HIGH SCORE
                self.max_boxlayout.add_widget(Label(text = str(self.a["Nom"]), color = (1, 0, 0, 1)))
                self.max_boxlayout.add_widget(Label(text = str(self.a["Score"]), color = (1, 0, 0, 1)))
                self.max_boxlayout.add_widget(Label(text = str(self.a["Temps"]), color = (1, 0, 0, 1)))
                self.max_boxlayout.add_widget(Label(text = str(self.a["Niveau"]), color = (1, 0, 0, 1)))

            else:
                self.max_boxlayout.add_widget(Label(text = 'HIGH SCORE', color = (1, 0, 0, 1))) #Met des bares si pas de scores
                self.max_boxlayout.add_widget(Label(text = "/", color = (1, 0, 0, 1)))
                self.max_boxlayout.add_widget(Label(text = "/", color = (1, 0, 0, 1)))
                self.max_boxlayout.add_widget(Label(text = "/", color = (1, 0, 0, 1)))
                self.max_boxlayout.add_widget(Label(text = "/", color = (1, 0, 0, 1)))

            a = 0
            for i in trans["Content"]: #Affiche les scores (max 10)
                a+=1

                if a<10 :
                    box = BoxLayout(orientation='horizontal')
        
                    box.add_widget(Label(text = i['Etat']))
                    box.add_widget(Label(text = i['Nom']))
                    box.add_widget(Label(text = str(i['Score'])))
                    box.add_widget(Label(text = str(i['Temps'])))
                    box.add_widget(Label(text = str(i['Niveau'])))

                    self.list_boxlayout.add_widget(box)


    def quit(self): #Methode pour quitter par le ficher kv
        sys.exit(0)


JeuApp().run()