# Code l'aspect graphique du jeu, les elements graphiques et d'interface graphique. 

import pygame
from math import *
from Pygame_commands import *
from Sound_design import *

class Couleur :
    """ Les couleurs de l'interface. Les attributs sont les suivants :\n RGB = [R,G,B]\nNom = "Nom de la couleur" """

    def __init__(self, nom, RGB):
        """ Constructeur de la classe Couleur. """
        # Attributs
        self.nom = nom
        self.RGB = RGB
        
    def __str__(self):
        return self.nom 
    
# Initialisation des differentes couleurs dans le jeu. 
Marron = Couleur("Raw Sienna", [220, 130, 71])
Cyan = Couleur("Cyan", [0,255,255])
Jaune = Couleur("Jaune", [255,255,0])
Vert = Couleur("Malachite", [59, 216, 101])
Rouge = Couleur("Rouge", [255,0,0])
Bleu = Couleur("Bleu",[0,0,255])
Noir = Couleur("Noir", [0,0,0])
Blanc = Couleur("Blanc", [255,255,255])
Gris = Couleur("Gris fonce", [130,130,130])

class User_Interface:
    """ Les elements d'interface graphique du jeu (boutons, cadre, retangles de conversation etc.).\n\nLes methodes : widow_draw_rect | hover_check | ecrire | background | transition_debut | transition_fin """

    def __init__(self):
        """ Le constructeur de la classe. """
        self.couleur = Blanc.RGB # Couleur de l'objet
        self.alpha = 155 # Transparence de l'objet
        self.surface = int() # Surface de l'objet
        self.texte = str()
        self.texte_pos_XY = []
        self.hover_state = False
        self.disponible = True
        self.background_disponibles = ["Bar", "BGai", "Port", "Arcade"]

    def window_draw_rect(self, PositionX, PositionY, Largeur, Hauteur):
        """ Dessine un rectangle. \n\nColor : [R,G,B] | Alpha (0-255)\n\nExemple d'utilisation : CTA.window_draw_rect(50,50,150,150) """

        # Dessine les bordures du rectangle
        Epaisseur = 5 # Pixels        

        # Dessine le fond du rectangle
        s = pygame.Surface((Largeur + Epaisseur, Hauteur + Epaisseur), pygame.SRCALPHA)   # alpha par pixel
        s.fill((0,0,0,self.alpha))                                # remarquez la valeur alpha dans les couleurs
        jeu.screen.blit(s, (PositionX,PositionY))

        # Permet d'enregistrer la nouvelle surface de l'objet
        self.surface = s.get_rect(topleft=(PositionX, PositionY))

        # Bordure Haute, Droite, Gauche, Basse
        # pygame.draw.rect(jeu.screen, self.couleur, (PositionX, PositionY, Largeur, Hauteur), Epaisseur)
        pygame.draw.rect(jeu.screen, self.couleur, (PositionX, PositionY, Largeur, Epaisseur))
        pygame.draw.rect(jeu.screen, self.couleur, (PositionX + Largeur, PositionY, Epaisseur, Hauteur))
        pygame.draw.rect(jeu.screen, self.couleur, (PositionX, PositionY, Epaisseur, Hauteur))
        pygame.draw.rect(jeu.screen, self.couleur, (PositionX, PositionY + Hauteur, Largeur + Epaisseur, Epaisseur))

    @property
    def hover_check(self):
        """ Verifie lorsqu'on passe en hover sur le bouton / l'objet.\n\nExemple d'utilisation : CTA.hover_check """

        # Si la souris est disponible et si le bouton est disponible
        if self.disponible and souris.disponible:
            # Si on est en hover
            if self.surface.collidepoint(souris.pos[0], souris.pos[1]) and self.disponible:
                self.couleur = Marron.RGB
                self.hover_state = True
            # Si on n'est pas en hover
            else :
                self.couleur = Blanc.RGB
                self.hover_state = False
        # Si c'est indisponible car on a deja clique dessus
        else :
            self.couleur = Gris.RGB
            self.hover_state = False
        
    @property
    def cliquer(self):
        """ Ce qui se passe lorsqu'on clique sur l'objet. """

        if self.hover_state and souris.click:
            SFX.jouer("Click", 0)
            return True
    
    def ecrire(self, texte, graisse, taille, position):
        """ Permet d'ecrire quelque chose a l'ecran.\n\n=> Graisses disponibles : Black, ExtraBold, Bold, SemiBold, Medium, Regular,  ExtraLight, Thin\n\n=> Exemple d'utilisation : CTA.ecrire("Bonjour", "Thin", 20, (10,10)) """

        self.texte = str(texte)
        self.texte_pos_XY = position

        # Police d'ecriture
        font = pygame.font.Font(f'Assets/Police/robotoSlab-{graisse}.ttf', taille)

        # Sous quelle forme va apparaitre le texte
        afficher = font.render(texte, True, self.couleur) 
        jeu.screen.blit(afficher, self.texte_pos_XY)

    def background(self, fond):
        """ Permet de mettre un fond.\n\nLes fond disponibles : Bar | Port\n\nExemple d'utilisation : UI[0].background("Bar") """

        # Background 
        background_image = pygame.image.load(f'Assets/Background/{fond}.png')

        # Depose l'image du background sur l'ecran. 
        jeu.screen.blit(background_image, (0,0))

    @property
    def transition_debut(self):
        """ Les transitions d'ecran. """

        # Desactive la souris
        souris.disponible = False

        # Fait glisser un rectangle noir sur tout l'ecran de haut en bas jusqu'a le recouvrir entierement. 
        for i in range(61):
            jeu.quit
            pygame.draw.rect(jeu.screen, Noir.RGB, (0, i * 10 - 600, 1000, 600))

            # Met a jour l'affichage de l'ecran.
            pygame.display.update()

            # Block le nombre de refreshrate a 60 fps.
            jeu.clock.tick(60)
        
        # Attend 1 seconde
        chrono.debut_timer
        while chrono.decompte(1) > 0:
            jeu.quit

        souris.disponible = True
            
    def transition_fin(self, pos_Y):
        """ Les transitions sortant d'ecran. L'idee est d'augmenter pos_Y jusqu'a 600. """

        # Dessine un ecran noir. 
        pygame.draw.rect(jeu.screen, Noir.RGB, (0, pos_Y, 1000, 600))
        
        # Si le rectangle noir sort de l'ecran, la souris redevient disponible. 
        if pos_Y >= 600:
            souris.disponible = True

    def reset_disponibilite(self, objet):
        """ Permet de remettre a 0 les disponibilites. """

        for i in objet:
            i.disponible = True


# Initialisation des elements d'interface
UI = [User_Interface() for i in range(15)]

# Initialisation des call to action
CTA = [User_Interface() for i in range(14)]
