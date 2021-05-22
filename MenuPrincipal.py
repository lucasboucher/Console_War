import pygame
from User_interface import *
from pygame import *
from Pygame_commands import *
from Choix_Personnage import *
from Menu_Aide import *

class MenuPrincipal:

    def __init__(self):
        """ Constructeur de la classe MenuPrincipal. """
        # Attributs
        self.Jouerj = ["Jouer", "Aide", "Quitter"]

        self.running = True

    @property
    def update(self):
        ''' Permet d'arriver dans le Menu Principal '''

        # Reset l'etat de la boucle du menu principal
        self.running = True

        # Verifie si on joue deja ou non la musique du menu principal. 
        if musique.nom != "BGai":
            musique.jouer("BGai", -1)

        # Reset la disponibilite de tous les CTA (Call to Action). 
        for i in CTA:
            i.disponible = True

        while self.running:
            # appliquer la fenetre du jeu
            UI[0].background("BGai")
            jeu.quit
            
            # Rectangle représentant le nom du jeu
            souris.pos_souris
            UI[0].ecrire("Console War", "Black", 60, (325, 60))

            self.rectangle()
            self.Jouer
            self.Aide
            self.Quitter()

            # Met a jour l'affichage de l'ecran.
            pygame.display.update()

            # Block le nombre de refreshrate a 60 fps.
            jeu.clock.tick(60)

    def rectangle(self):
        '''Dessine les rectangles et les mots du Menu Principal.'''
        
        for i in CTA:
        
            if CTA.index(i) > 2:
                break

            # Dessine les rectangles pour les mots
            i.window_draw_rect(360, (CTA.index(i)+ 1) * 90 + 130, 300, 75)
            
            mot = self.Jouerj[CTA.index(i)]

            # Permet d'ecrire les differents mots et de passer en hover dessus
            i.ecrire(mot, "Medium", 36, (385, (CTA.index(i)+ 1) * 90 + 140))
            i.hover_check

    def Quitter(self):
        ''' Permet de quitter le jeu quand on appuie sur "Quitter".'''
        if CTA[2].cliquer:
            UI[0].transition_debut
            pygame.quit()
            exit()

    @property
    def Aide(self):
        """ Lance le menu aide. """
        if CTA[1].cliquer:
            self.running = False
            menu_aide.update

    @property
    def Jouer(self):
        ''' Permet de lancer le jeu lorsqu'on appuie sur le bouton "Jouer" '''
        if CTA[0].cliquer:
            self.running = False
            choix_personnage.update

menu = MenuPrincipal()