# La grosse boucle du jeu se trouve ici. Lance tout ce qu'il faut lancer

from MenuPrincipal import *
from Combat import *

# Boucle du jeu
running = True

while running:

    menu.update

    if choix_personnage.combat:
        lancement_combat()
        choix_personnage.combat = False

    jeu.quit