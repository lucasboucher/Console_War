# Code le systeme de combat.

import pygame, random
from User_interface import *
from Pygame_commands import *
from Sound_design import *
from Personnages import *
from Insulte_consoles import *
from math import *
from Choix_Personnage import *


class Joueur:
    """ La classe du joueur. """

    def __init__(self, nom, num_joueur, personnage):
        """ Les attributs : nom = str() | num_joueur = 1 (gauche) ou 2 (droite) \n\nLes personnages (en string) : Switch, Playstation, Xbox, Arcade, PC """
        self.sante_max = int()
        self.mots = []
        self.phrase = str()
        self.construction = [] # Decortique chaque categorie des mots dans la phrase pour la correction. 
        self.nom = nom
        self.num_joueur = num_joueur # Le joueur 1 est a gauche, le joueur 2 est a droite. 
        self.personnage = personnage # Le personnage qui sera utilise par le joueur en question. 
        self.faiblesse = []
        self.resistance = []
        self.IA = False

        self.idex = int() # L'index du personnage dans la liste consoles. 

        # Enregistre les faiblesses, resistance et la sante max de notre personnage
        for console in consoles:
            if self.personnage == console.nom:
                self.faiblesse = console.faiblesse
                self.resistance = console.resistance
                self.sante_max = console.sante
                self.index = consoles.index(console)

        # Fixe la sante actuelle a la sante max lors de l'initialisation
        self.sante_actuel = self.sante_max
        self.ratio_sante = self.sante_actuel / self.sante_max

    @property
    def combi_mot(self):
        """ Permet de combiner les mots pour faire une phrase. """

        # Vide la phrase pour pouvoir eviter une repetition de mots. 
        self.phrase = str()
        # Concataine les mots dans la phrase. 
        for mot in self.mots:
            self.phrase += " " + mot

    @property
    def categorisation(self):
        """ Categorise chaque mot de la phrase. En outre, dit pour chaque mot si c'est un adjectif, verbe, sujet, fin de phrase ou mot de liaison et puis range la categorie du mot au sein d'une liste. """

        # Vide la liste de construction pour eviter une repetition de categories. 
        self.construction = []
        # On va passer sur tous les elements de la liste "mots" pour les categoriser
        for mot in self.mots:
            for key, value in insultes.items(): # Verification de la categorie du mot. 
                if mot in value:
                    self.construction.append(key)

    @property
    def correction(self):
        """ Verifie si les categories sont positionnes au bon endroit l'un par rapport a l'autre dans la phrase. """

        # Le coefficient qui sera utilise pour pouvoir calculer les degats qu'on inflige. 
        coefficient = 1

        # mot en position i-1
        pos1_mot = str()
        # mot en position i
        pos2_mot = str()

        if len(self.construction) == 0:
            return 0

        # Verifie si la derniere categorie est une terminaison de phrase. 
        if self.construction[len(self.construction)-1] == "fins":
            coefficient += 0.4

        # Si on ne commence pas par un sujet notre phrase, on est penalise. 
        if self.construction[0] != "sujets" :
            coefficient -= 0.1

        for i in self.construction[1:]:
            pos1_mot = self.construction[self.construction.index(i)-1]
            pos2_mot = i

            # Dans le cas ou le premier mot analyse est un sujet
            if pos1_mot == "sujets" and not (pos2_mot == "adjectifs" or pos2_mot == "verbes" or pos2_mot == "liaisons"):
                coefficient -= 0.2
            
            # Dans le cas ou le premier mot est un verbe
            if pos1_mot == "verbes" and not (pos2_mot == "laisons" or pos2_mot == "fins"):
                coefficient -= 0.2

            # Dans le cas ou le premier mot analyse est un adjectf
            if pos1_mot == "adjectifs" and not (pos2_mot == "verbes" or pos2_mot == "liaisons"):
                coefficient -= 0.2

            # Dans le cas ou le premier mot analyse est un mot de liaison
            if pos1_mot == "liaisons" and pos2_mot != "sujets":
                coefficient -= 0.2

            # Dans le cas ou le premier mot analyse est une terminaison de phrase
            if pos1_mot == "fins":
                coefficient -= 0.2
                
        return coefficient

    def calcul_degats(self, mots):
        """ Calcul des degats qu'on recoit """

        # Multiplicateur de degats
        coefficient = self.correction

        # Les degats qu'on va infliger
        longueur_phrase = len(self.phrase) * 0.25

        # Verifie si les mots qu'on recoit son presents dans nos faiblesses ou resistances
        for mot in mots:
            if mot in self.faiblesse:
                coefficient += 0.4
            elif mot in self.resistance:
                coefficient -= 0.2
        
        # Calcul les degats. 
            # Plus notre phrase est longue, plus on fait de degats. 
            # Plus on a de mots pertinents, plus on fait de degats. 
            # Moins on fait de fautes de francais, plus on fait des degats. 
        degats = ceil(longueur_phrase * coefficient)

        return degats

    @property
    def vider(self):
        """ Permet de vider les mots dans la phrase du joueur, mais aussi sa phrase. """
        self.mots = []
        self.phrase = str()

class Combat:

    def __init__(self):
        # self.round = int()
        self.background = UI[0].background_disponibles[random.randrange(0, 4)]

        # Permet de savoir c'est le tour de quel joueur. Si self.nombre_tour % 2 = 0, c'est au tour du joueur 1 et si ca vaut 2, c'est au tour du joueur 2.
        self.nombre_tours = -1 

        # Moins le joueur a de sante, moins il a le temps pour decider de son prochain mot. Index 0 = joueur 1 (de gauche) et Index 1 = joueur 2 (de droite)
        self.chronometre = [int(), int()] 

        self.mot_disponibles = {} # 14 mots max, dit si le mot est utilise (= True) ou pas(= False). {"Mot 1":True , "Mot 2":False}
        self.fin_combat = False
        self.round = 1

        self.highlight = [26, 26] # Un halo au tour du personnage qui doit choisir un mot. 

        # Affichage des degats. 
        self.degats_taille = 0 # La taille de la police des degats. 
        self.degats = [] # La quantite des degats.

        self.vainqueur = "Match nul" # Le nom du joueur qui gagne. 

    def mot_hasard(self, categorie):
        """ Genere un mot au hasard en fonction de sa categorie. """
        # On genere un nombre au hasard en fonction de la taille d'une liste de mots. 
        hasard = random.randrange(0, len(insultes[categorie]))
        # On renvoie le mot qui a genere aleatoirement. 
        mot = insultes[categorie][hasard]
        return mot
    
    @property
    def ajout_mot(self):
        """ Ajoute des mots a la liste de mots dans le tour. """

        # Compteur de mots pour chaque categorie, permet de faire en sorte que le dernier mot ne soit pas repete. 
        num_item = {"sujets":int(), "verbes":int(), "fins":int(), "liaisons":int(), "adjectifs":int()}

        # Liste qui permet de faire en sorte qu'aucun mot hormis le dernier soit repete. 
        liste = []

        # Reset la liste des mots disponibles.
        self.mot_disponibles = {}

        # Permet d'ordonner les mots au sein du dictionnaire self.mot_disponibles. 
            # Ordonner les mots va permettre de les affichier a l'ecran dans un ordre precis par la suite. 
        count = int()

        # Ajout des mots dans la liste de mots disponibles. On va ajouter seulement 3 mots max par categorie. 
        for keys in insultes.keys():

            while num_item[keys] < 3:
                # On va piocher un mot au hasard. 
                mot = self.mot_hasard(keys)

                if mot not in liste:
                    # On va l'inserer dans le dictionnaire. 
                    liste.append(mot)
                    self.mot_disponibles[mot] = ["False", str(count)]
                    num_item[keys] += 1
                    count += 1
    
    @property
    def fin_de_phase(self):
        """ Inflige des degats en fin de phase et passe a la phase suivante. """
        
        # Les degats recus : [provenant du joueur 2 , provenant du joueur 1]
        self.degats = [joueur[1].calcul_degats(joueur[0].mots) ,joueur[0].calcul_degats(joueur[1].mots)]
        SFX.jouer(f"Hit{random.randrange(1,2)}", 0)

        # Inflige les degats aux joueurs
        for i in range(2):
            joueur[i].sante_actuel -= self.degats[i]
            joueur[i].ratio_sante = joueur[i].sante_actuel / joueur[i].sante_max

            # Le cas ou un joueur tombe en dessous de 0 point de vie. 
            if joueur[i].sante_actuel < 0:
                joueur[i].sante_actuel = 0
                self.fin_combat = True

                # Attribut le nom du vainqueur a celui qui a encore de la sante. 
                if joueur[0].sante_actuel == 0 and joueur[1].sante_actuel == 0 :
                    self.vainqueur = "Match nul !"
                    self.highlight = [25, 25]
                elif joueur[0].sante_actuel > 0:
                    self.vainqueur = f"{joueur[0].nom} est le vainqueur !"
                    self.highlight = [50, 0]
                else :
                    self.vainqueur = f"{joueur[1].nom} est le vainqueur !"
                    self.highlight = [0, 50]

        # Dessine les degats et passe a la phase suivante. 
        self.degats_taille = 50

        self.nouvelle_phase

    @property
    def nouvelle_phase(self):
        """ Permet de passe a une nouvelle phase du combat. Une phase correspond au fait d'avoir de nouveaux mots parmi lesquels on peut choisir et aussi au fait de devoir formuler une nouvelle phrase. """

        # Remet a jour la disponibilite des mots
        for i in CTA:
            i.disponible = True
        
        if self.fin_combat != True:
            # Remet de nouveaux mots parmi lesquels choisir. 
            self.ajout_mot
        
        # Reinitialise les phrases des 2 joueurs. 
        for i in joueur:
           i.vider 

    @property
    def dessine_mot(self):
        """ Permet de dessiner les mots a l'ecran. """

        # Compteur utilise pour ordonner les mots au sein du dictionnaire self.mot_disponibles
        count = int()
        # Les mots qui vont etre ecrits sur l'ecran et manipules. 
        mot = str()

        # Position X des insultes et du cadre. 
        pos_X = 338

        # Dessine le cadre sur lequel sera dessine les mots. 
        UI[1].window_draw_rect(pos_X, 170, 320, 500)

        # On va passer en revu tous les objets de la liste CTA
        for i in CTA:
            
            # Permet de gerer la zone cliquable des mots. 
            i.surface = pygame.Rect(pos_X, (CTA.index(i)+ 1) * 29 + 150, 310, 25 )
            # Associe un mot du dictionnaire mot_disponibles a un objet de la liste CTA. 
            for j,k in self.mot_disponibles.items():
                if str(count) in k[1]:
                    mot = j
                    count += 1
                    break
            # Permet d'ecrire les mots. 
            i.ecrire(mot, "Medium", 21, (pos_X + 18, (CTA.index(i)+ 1) * 29 + 150))
            # Permet de verifier si on passe en hover sur les mots. 
            i.hover_check

    def clique_mot(self, joueur):
        """ Ce qui se passe lorsqu'on clique sur un mot.\n\nParametres : joueur = liste """
        
        for i in CTA:
            # On clique sur le mot et le mot n'est pas encore utilise
            if i.cliquer and self.mot_disponibles[i.texte][0] == "False":
                self.mot_disponibles[i.texte][0] = "True" # Devient utilise
                joueur.mots.append(i.texte) # Ajout du mot a la liste du personnage
                i.disponible = False
                joueur.combi_mot
                joueur.categorisation

                # Apres avoir selectionne un mot, debute un nouveau tour. 
                self.nouveau_tour

    @property
    def dessine_highlight(self):
        """ Dessine un highlight au tour du personnage. """
        # Dessine le fond du rectangle
        s = pygame.Surface((175, 600), pygame.SRCALPHA)   # alpha par pixel
        s.fill((255,255,0 ,self.highlight[0]))                                
        jeu.screen.blit(s, (75,0))

        s2 = pygame.Surface((175, 600), pygame.SRCALPHA)   # alpha par pixel
        s2.fill((255,255,0 ,self.highlight[1]))                              
        jeu.screen.blit(s2, (745,0))

    @property
    def calcul_highlight(self):
        """ Calcule la valeur alpha des halo. """
        
        if self.highlight[0] < 50 and self.nombre_tours % 2 == 0:
            self.highlight[0] += 2
            self.highlight[1] -= 2
        elif self.highlight[1] < 50 and self.nombre_tours % 2 == 1 : 
            self.highlight[0] -= 2
            self.highlight[1] += 2

        self.dessine_highlight

    @property
    def dessine_interface(self):
        """ Permet de dessiner la phrase du joueur a l'ecran. Dessine aussi la barre de sante. """
        
        # Affiche le rectangle du joueur 1 et 2 respectivement permettant d'afficher les phrases qui se construisent. 
        UI[2].window_draw_rect(-5, 90, 830, 40)
        UI[2].ecrire(joueur[0].phrase, "Bold", 20, (10, 98))
        Barredevie1.dessiner(1)
        
        UI[3].window_draw_rect(175, 130, 830, 40)
        UI[3].ecrire(joueur[1].phrase, "Bold", 20, (193, 138))
        Barredevie2.dessiner(2)

        # Affiche quand les mots s'envoit
        UI[8].window_draw_rect(690, -5, 310, 45)
        if self.fin_combat != True:
            UI[8].ecrire(f"Envoi des phrases dans {9 - self.nombre_tours % 9} tours", "Bold", 20, (700, 7))

        # Affiche les degats
        UI[6].couleur, UI[7].couleur = Jaune.RGB, Jaune.RGB
        if self.degats_taille > 0 and self.nombre_tours > 0:
            UI[6].ecrire(str(-self.degats[0]), "Bold", ceil(self.degats_taille), (240, 15 + abs(self.degats_taille - 30)))
            UI[7].ecrire(str(-self.degats[1]), "Bold", ceil(self.degats_taille), (900, 117 + abs(self.degats_taille - 30)))
            self.degats_taille -= 2

        # Dessine les personnage a l'ecran et le nom du joueur. 
        for i in range(2):
            UI[10 + i].window_draw_rect(70 + i * 666, 547, 180, 60)
            UI[10 + i].ecrire(joueur[i].nom, "Bold", 30, (85 + i * 666, 555))
            consoles[joueur[i].index].dessiner_personnage(88 + i * 672, 240, i)

    @property
    def retour_menu(self):
        """ Code le bouton permettant de revenir au menu principal. """

        UI[12].window_draw_rect(-5, -5, 130, 50)
        UI[12].ecrire("Retour", "Bold", 30, (15, 0))

        UI[12].hover_check
        if UI[12].cliquer:
            self.fin_combat = True

    @property  
    def time_check(self):
        """ Verifie si le joueur a depasse le temps pour choisir son mot. Si oui, il passe son tour. """

        if chrono.decompte(self.chronometre[self.nombre_tours % 2]) == 0:
            self.nouveau_tour

    @property
    def temps_max(self):
        """ Calcul le temps que le joueur a pour choisir ses mots. Moins il a de sante, moins il aura de temps. \n\nL'argument : joueur = 1 (joueur de gauche) | joueur = 2 (joueur de droite)"""
        
        # On va verifier le pourcentage de sante qu'il reste pour chaque joueur. S'il ne reste plus beaucoup de vie, on n'a plus que 3 secondes pour choisir son mot. 
        if joueur[self.nombre_tours % 2].ratio_sante > 0.5:
            self.chronometre[self.nombre_tours % 2] = floor(joueur[self.nombre_tours % 2].ratio_sante * 10)
        else:
            self.chronometre[self.nombre_tours % 2] = 5

    @property
    def afficher_chrono(self):
        """ Permet d'afficher le chronometre a l'ecran. """ 
        self.temps_max

        if chrono.decompte(self.chronometre[self.nombre_tours % 2]) <= 3 :
            UI[5].couleur = Rouge.RGB
            taille = 80
            pos_Y = -10
        else :
            UI[5].couleur = Blanc.RGB
            taille = 65
            pos_Y = 0

        UI[5].ecrire(str(chrono.decompte(self.chronometre[self.nombre_tours % 2])), "Bold", taille, (490, pos_Y))

    @property
    def nouveau_tour(self):
        """ Debute un nouveau tour. """

        # Augmente le nombre du tour de 1
        self.nombre_tours += 1
        # Reset le timer
        chrono.debut_timer

        # Si le nombre de tour dans une phase atteint 9, on envoie les mots et on passe a la phase suivante. 
        if self.nombre_tours % 9 == 0 and self.nombre_tours > 1:
            self.fin_de_phase

    # @property
    # def round_check(self):
    #     """ Gere le systeme de round. """

    #     if joueur[1].IA:
    #         # Affiche le round
    #         UI[4].window_draw_rect(830, -5, 200, 45)
    #         UI[4].ecrire(f"Round {self.round}", "Bold", 30, (848, -3))

    #         # Les conditions de fin de round.
    #         if joueur[1].IA and joueur[1].sante_actuel == 0 :
    #             self.round += 1
            
    @property
    def animation_rentrant(self):
        """ L'animation de transition rentrant pour le combat. """

        souris.disponible = False

        for i in range(61):

            UI[0].background(self.background)

            # Permet de coder la croix pour quitter le jeu. 
            jeu.quit

            # Dessine les highlights au tour du personnage qui gagne. 
            self.dessine_highlight

            # Le fond.
            self.dessine_mot
            self.dessine_interface
            self.retour_menu

            # La fenetre qui annonce le vainqueur. 
            UI[0].transition_fin(i * 10)

            # Met a jour l'affichage de l'ecran.
            pygame.display.update()

            # Block le nombre de refreshrate a 60 fps.
            jeu.clock.tick(60)

        souris.disponible = True

    @property
    def fin(self):
        """ La fin, lorsque l'un des joueurs n'a plus de sante. """

        # Desactive les clics de la souris. 
        souris.disponible = False

        self.mot_disponibles = {}
        UI[9].alpha = 255

        if self.vainqueur != "Match nul":
            musique.jouer("Victoire", 0)
        else:
            musique.jouer("Match_nul", 0)

        for i in range(-3, 17):

            UI[0].background(self.background)

            # Permet de coder la croix pour quitter le jeu. 
            jeu.quit

            # Dessine les highlights au tour du personnage qui gagne. 
            self.dessine_highlight

            # Le fond.
            self.dessine_mot
            self.dessine_interface

            # La fenetre qui annonce le vainqueur. 
            UI[9].window_draw_rect(250, i * 15, 500, 100)
            UI[9].ecrire(self.vainqueur, "Bold", 30, (270, i * 15 + 30))

            # Met a jour l'affichage de l'ecran.
            pygame.display.update()

            # Block le nombre de refreshrate a 60 fps.
            jeu.clock.tick(60)

        # Attend 2 seconde
        chrono.debut_timer
        while chrono.decompte(3) > 0:
            jeu.quit

    @property
    def update(self):
        """ La boucle de la classe, update d'ecran et l'etat de chaque element a l'ecran. """
        
        musique.jouer(self.background, -1)
        self.animation_rentrant
        self.fin_combat = False
        
        while self.fin_combat != True:

            UI[0].background(self.background)

            # Permet de coder la croix pour quitter le jeu. 
            jeu.quit

            # Calcul la position de la souris
            souris.pos_souris

            # Dessine les highlights pour voir c'est le tour de qui. 
            self.calcul_highlight

            self.time_check
            self.dessine_mot
            self.clique_mot(joueur[self.nombre_tours % 2])
            self.dessine_interface
            # self.round_check
            self.afficher_chrono
            self.retour_menu
            
            # Met a jour l'affichage de l'ecran.
            pygame.display.update()

            # Block le nombre de refreshrate a 60 fps.
            jeu.clock.tick(60)

        self.fin
        UI[0].transition_debut

# barre de vie des joueurs. Source : https://www.youtube.com/watch?v=pUEZbUAMZYA
class BarreDeSante:

    def __init__(self, joueur):
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.current_health = joueur.sante_actuel
        self.target_health = joueur.sante_actuel
        self.maximum_health = joueur.sante_max
        self.health_bar_length = 330
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 5

    # Lorsqu'on se prend des damages
    def get_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0
            
    def dessiner(self, joueur_type): 

        # Positionnement des barres de sante en fonction du joueur. (1 = joueur de gauche, 2 = joueur de droite)
        if joueur_type == 1:
            X = 10
            Y = 68
            self.target_health = joueur[0].sante_actuel
        else:
            X = 660
            Y = 173
            self.target_health = joueur[1].sante_actuel

        # Animation de la barre jaune qui descend 
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed

        # Dimension de la barre rouge
        health_bar_rect = pygame.Rect(X,Y,self.target_health/self.health_ratio,25) 

        # Barre jaune
        pygame.draw.rect(jeu.screen,Jaune.RGB,(X,Y,self.current_health / self.health_ratio,25))

        # Barre Rouge
        pygame.draw.rect(jeu.screen,Vert.RGB,health_bar_rect)

        # Contours blancs
        pygame.draw.rect(jeu.screen,Blanc.RGB,(X,Y,self.health_bar_length,25),4)

def lancement_combat():
    """ Lance le combat. """
    global joueur, Barredevie1, Barredevie2

    # Initialisation des joueurs
    joueur = [
    Joueur(choix_personnage.joueur1[0], choix_personnage.joueur1[1], choix_personnage.joueur1[2]),
    Joueur(choix_personnage.joueur2[0], choix_personnage.joueur2[1], choix_personnage.joueur2[2])
    ]

    combat = Combat()
    combat.nouvelle_phase

    # Initialisation de la bare de vie
    Barredevie1 = BarreDeSante(joueur[0])
    Barredevie2 = BarreDeSante(joueur[1])

    combat.update
