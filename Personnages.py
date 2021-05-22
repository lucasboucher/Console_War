# Code les personnages du jeu en listant leurs caracteristiques.

import pygame
from Pygame_commands import *

class Personnages:
    '''Classe des personnages'''

    def __init__(self, nom, sante, resistance, faiblesse, desc):
        '''Constructeur de la classe'''
        self.nom = str(nom)
        self.sante = sante 
        self.resistance = resistance
        self.faiblesse = faiblesse
        self.sprite_gauche = pygame.image.load(f'Assets/Sprite/{self.nom}_gauche.png')
        self.sprite_droite = pygame.image.load(f'Assets/Sprite/{self.nom}_droite.png')
        self.desc = desc
        
    def __str__(self):
        return self.nom 

    def dessiner_personnage(self, pos_X, pos_Y, joueur):
        """ Dessine le personnage sur l'ecran. \n\nLes parametres : pos_X = int(position X) | pos_Y = int(position Y) | joueur = int(0) = gauche ou int(1) = droite """
        if joueur == 0:
            jeu.screen.blit(self.sprite_gauche, (pos_X,pos_Y))
        else:
            jeu.screen.blit(self.sprite_droite, (pos_X,pos_Y))

# Initialisation des differents personnages dans le jeu. 
consoles = [
Personnages("Switch", 90, ["decroit a vue d'oeil", "ta popularite"], [], ["La derniere console de chez","Nintendo, console fixe comme","portable.","","Points forts :","- Tres populaire","- Ne viellit pas","","","",""]),
Personnages("Playstation", 110, ["payant"], ["ta duree de vie", ], ["Les consoles de chez Sony font","parti depuis 1994 des consoles","les plus vendus au monde.","","Points fort :","- Pas cher","","Points faible :","- Duree de vie courte","",""]),
Personnages("Xbox", 110, ["permet rien", "payant"] , ["decroit a vue d'oeil", "ta duree de vie", ], ["La même année que pour Sony,","Xbox de Microsfot va devenir","une console fixe mythiques.","","Points forts :","- Pas cher","- Beaucoup de fonctionnalités","","Points faibles :","- Ventes en baisse","- Courte durée de vie"]),
Personnages("Arcade", 140, [ "ta batterie", "tes exclusivites"], ["ton Online", "vieux"], ["Les jeux arcades font partis des","ancêtres et des fondamentaux","des consoles next-gen.","","Points forts :","- Beaucoup de batterie","- Jeux exclusifs","","Points faibles :","- Pas de multijoueur","- Vielles technologies"]),
Personnages("PC", 150, ["ta popularite"], ["trop cher", "vieux"], ["Le PC permet de presque tout","faire et comme les consoles de","jouer aux jeux vidéo.","","Points fort :","- Très populaire","","Points faibles :","- Très cher","- Est très vieux",""])
]

# Cdi = Personnages("Cdi", 100, ["mechant","jeune"], ["nouvelle","ancienne"])
# Gamecube = Personnages("Gamecube", 100, ["mechant","jeune"], ["nouvelle","ancienne"])
# Dreamcast = Personnages("Dreamcast", 100, ["mechant","jeune"], ["nouvelle","ancienne"])
