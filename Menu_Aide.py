from User_interface import *
from Personnages import *

class Menu_Aide:

    def __init__(self):
        self.switch_layout = True #True = Layout Regles / False = Layout Personnages
        self.sante = "Erreur" #Definition de la vraible "sante", si n'apparait pas affiche "Erreur"

        self.running = True

    @property
    def layout_rules(self):
        #Definition des variables "titre" et "desc", ici pour l'affchage des regles
        self.titre = "Regles"
        self.desc = ["Votre objectif est d'insulter votre","adversaire de la façon la plus","bien ecrite possible et avec les","mots les mieux choisi.","","L'equipe de developpement vous","souhaite bonne chance pour","vaincre l'ordinateur !","","",""]
        
        
        #Panneau des informations generales (droite)
        UI[2].window_draw_rect(50, 200, 600, 350) #Fond
        x = 215
        for i in range(11):
            UI[2].ecrire(self.desc[i], "Medium", 23, (70,x))
            x += 30
        
        #Panneau de titre
        UI[3].window_draw_rect(50, 150, 600, 50) 
        UI[3].ecrire(self.titre, "Bold", 25, (70,160))

        #Le bouton des regles grise
        CTA[6].disponible = False
    
    @property
    def layout_perso(self):

        #Remise a 0 des boutons perosnnages grise
        for i in range(5):
            CTA[i].disponible = True

        #Interface de texte
        UI[1].window_draw_rect(50, 150, 200, 400) #Panneau lateral d'illustration (gauche)
        UI[1].ecrire("Vie :", "Medium", 25, (70,505))
        UI[1].couleur = Vert.RGB
        UI[1].ecrire(self.sante, "Bold", 25, (130,505))
        UI[1].couleur = Blanc.RGB
        
        #Panneau des informations generales (droite)
        UI[2].window_draw_rect(250, 200, 400, 350) #Fond
        x = 215
        for i in range(11):
            UI[2].ecrire(self.desc[i], "Medium", 23, (270,x))
            x += 30
        
        #Panneau de titre
        UI[3].window_draw_rect(250, 150, 400, 50) 
        UI[3].ecrire(self.titre, "Bold", 25, (270,160))

        #Bouton regle degrise
        CTA[6].disponible = True

        #Mise a jour des informations pour chaque personnage
        for i in range(5):
            if self.perso_number == i+1:
                Joueur = consoles[i]
                Joueur.dessiner_personnage(75,200,0)
                self.titre = Joueur.nom
                self.desc = Joueur.desc
                self.sante = f"{Joueur.sante}"
                CTA[i].disponible = False

    @property
    def navigation(self):
        #Fond du choix du menu d'aide
        UI[4].window_draw_rect(750,155,200,400)   

        #Mise en place des personnages, separation, textes et zones
        for i in CTA:
            if CTA.index(i) > 4 :
                break
            Joueur = consoles[CTA.index(i)]
            i.ecrire(Joueur.nom, "Bold", 25, (770, CTA.index(i) * 80 + 175))
            i.surface = pygame.Rect(750, CTA.index(i) * 80 + 155, 175, 80)
            i.hover_check
            if i.cliquer:
                self.switch_layout = False
                self.perso_number = CTA.index(i) + 1
            pygame.draw.rect(jeu.screen, Blanc.RGB, (770, CTA.index(i) * 80 + 155, 160, 1))
            
        #Bouton des regles
        CTA[6].window_draw_rect(750, 50, 200, 90)
        CTA[6].hover_check
        CTA[6].ecrire("Regles", "Bold", 25, (810, 80))
        if CTA[6].cliquer:
            self.switch_layout = True
        
        #Bouton de retour
        CTA[5].window_draw_rect(50, 50, 200, 50)
        CTA[5].hover_check
        CTA[5].ecrire("Retour", "Bold", 25, (110, 60))

        if CTA[5].cliquer:
            self.running = False

   
    @property
    def update(self):
        # Boucle du jeu
        self.running = True

        while self.running:

            UI[0].background("BGai")

            # Permet de coder la croix pour quitter le jeu. 
            jeu.quit

            # Dessine un rectangle, si on passe en hover dessus ca change de couleur.
            souris.pos_souris

            self.navigation
            if self.switch_layout:
                self.layout_rules

            else:
                self.layout_perso
                
            # Met a jour l'affichage de l'ecran.
            pygame.display.update()

            # Block le nombre de refreshrate a 60 fps.
            jeu.clock.tick(60)

#Initialisation du menu aide pour test
menu_aide = Menu_Aide()
