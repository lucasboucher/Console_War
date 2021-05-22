# Code la souris et les interactions de la souris avec les differents elements du jeu. Code aussi certains aspects plus abstraits comme la sauvegarde de score en fin de partie pour le leader board etc. 

import pygame, pickle
from math import *

class Souris:
    """ Permet de cliquer et obtenir la position du curseur.\nMethodes : click, pos_souris """

    def __init__(self):
        self.pos = []
        self.disponible = True # Le souris devient indisponible a certains moments du jeu. 

    @property
    def click(self):
        """ Test si le joueur a clique ou non.\n\n Exemple d'utilisation : souris.click """

        left_click, right_click, middle_click = pygame.mouse.get_pressed()

        if self.time_check and left_click and self.disponible:
            chrono_souris.debut_timer
            return left_click

        # #Gere les input du joueur
        # for event in pygame.event.get():
        #     # Si un clic est pressee, le joueur valide.
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         return True

    @property
    def pos_souris(self):
        """ Met a jour les positions X et Y de la souris. """
        self.pos = pygame.mouse.get_pos()
        
    @property
    def time_check(self):
        """ Verifie s'il y a plus d'une seconde d'ecart entre nos clics. """

        chrono_souris.update_time
        timer = chrono_souris.temps_actuel - chrono_souris.debut_compte

        # On peut cliquer qu'apres 0.4 sec par rapport au clic precedent. 
        if 400 - timer < 0:
            return True
        else :
            return False

class Jeu :
    """ Les fonctions qui seront redondantes. """

    def __init__(self):
        # Initialise le pygame, se doit de toujours etre la
        pygame.init()

        # Initialise la classe qui permet d'utiliser des timers / le temps dans pygame avec un objet.
        self.clock = pygame.time.Clock()

        # Creer l'ecran du jeu
        self.screen = pygame.display.set_mode((1000,600)) # Les dimensions de l'ecran

        # Le nom du jeu
        self.nom_jeu = "Console War"

        # Chance l'icone du jeu. 
        icon = pygame.image.load('Assets/Icone_jeu.png') #Source : flaticon.com
        pygame.display.set_icon(icon)

        # Changer le titre de la fenetre
        pygame.display.set_caption(self.nom_jeu)

        # Etat du leader board actuel (fonctionnalite utilisee : sauvegarde)
        self.leader_board = {}

    @property
    def quit(self):
        """ Fonction qui permet de quitter le jeu. """

        #Gere les inputs du joueur
        for event in pygame.event.get():
            #Lorsqu'on clique sur fermer la fenetre
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    @property
    def valider(self):
        """Fonction qui va attendre que le joueur valide ce qu'il voit en cliquant. \n\nExemple d'utilisation : jeu.valider"""

        valider = False
        while valider == False:
            #Gere les input du joueur
            for event in pygame.event.get():
                #Si on souhaite fermer le jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # # Si la touche espace est pressee, le joueur valide et le combat passe a la phase suivante.
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     valider += 1

            valider = souris.click

    @property
    def sauvegarde(self):
        """Permet de sauvegarder l'avancee du jeu.\n\nExemple d'utilisation : jeu.sauvegarde"""

        with open("Donnees","wb") as folder: # with: manipule un objet (fichier dans notre cas), ferme le fichier a la fin  |  as: "en tant que"
        # Nous allons chercher a sauvegarder les donnees de l'objet leader_board dans un fichier.

            mon_pickler = pickle.Pickler(folder) # Operation qui sera execute
            mon_pickler.dump(self.leader_board)

    @property
    def charger(self):
        """Permet de charger une sauvegarde.\n\nExemple d'utilisation : jeu.charger"""

        with open("Donnees", "rb") as folder:
            # Nous allons chercher a acceder aux donnees presentes dans le fichier score.

            mon_depickler = pickle.Unpickler(folder) 
            load_score = mon_depickler.load()

        self.leader_board = load_score

        # for key, value in Sauvegarde_leader_board.items():
        #     self.leader_board[key] = value

class Chronometre:

    def __init__(self):
        """ Le chronometre. \n\nLes attributs sont les suivants : temps_acutel | debut_compte\n\nLes methodes : update_time | debut_timer | calcul_timer"""
        self.temps_actuel = int()
        self.debut_compte = int()

        # Commence le timer des l'initialisation de l'objet. 
        self.debut_timer
    
    @property
    def update_time(self):
        """ Met a jour le temps actuel. """
        self.temps_actuel = pygame.time.get_ticks()

    @property
    def debut_timer(self):
        """ Commence le compte d'un timer. Permet aussi de reset le timer. """
        self.debut_compte = pygame.time.get_ticks()

    @property
    def calcul_timer(self):
        """ Donne le temps du timer depuis le debut du compte en seconde. """
        self.update_time
        timer = floor((self.temps_actuel - self.debut_compte) / 1000)

        return timer

    def decompte(self, temps):
        """ Decompte a partir de la variable "temps" jusqu'a 0, avec chaque tick qui correspond a 1 seconde.\n\nArgument : temps (en seconde et integer) """

        timer = temps - self.calcul_timer
        if timer < 0:
            timer = 0

        return timer

# Initialisation des objets
souris = Souris()
jeu = Jeu()

# Chronometre du combat
chrono = Chronometre()

# Chronometre pour les clics de la souris
chrono_souris = Chronometre()

# Chronometre pour l'input (lorsque l'on nomme les joueurs)
chrono_input = Chronometre()