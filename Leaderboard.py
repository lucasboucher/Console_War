import pygame
from User_interface import *
from pygame import *
from Pygame_commands import *

class Leaderboard:
# Etat du leader board actuel (fonctionnalite utilisee : sauvegarde)
    def __init__(self):
        ''' Constructeur de la classe Leaderboard. '''
        # Attributs
        self.leader_board = {}
        self.retour_mot = ["Retour"]
    
    def update(self):
        running = True
        while running:
            # appliquer la fenetre du jeu
            UI.background("Bgai")
            jeu.quit
            
            # Rectangle représentant le nom du jeu
            UI.window_draw_rect(100,100,400,60)
            souris.pos_souris
            UI.hover_check

            self.retour()

            # Met a jour l'affichage de l'ecran.
            pygame.display.update()

            # Block le nombre de refreshrate a 60 fps.
            jeu.clock.tick(60)
    


    def retour(self):
        ''' Permet de revenir sur le Menu Principal '''

        # Dessine les rectangles pour les mots
        .window_draw_rect(420, (CTA.index(i)+ 1) * 90 + 130, 300, 75)

        mot = self.retour_mot[CTA.index(i)]

        # Permet d'ecrire les differents mots et de passer en hover dessus
        i.ecrire(mot, "Medium", 36, (445, (CTA.index(i)+ 1) * 90 + 140))
        i.hover_check


            

LB = Leaderboard()
LB.update()

    #def rank(self):
