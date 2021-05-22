from User_interface import *
from Personnages import *
from pygame import *

class Choix_Personnage:

    def __init__(self):

        # Des booleens qui controlent certains aspects de la selection des personnages. 
        self.switch_selection = True #True = Non sélectionné / False = personnage sélectionné
        self.selection = False # L'etat de l'input, si c'est selectionne ou pas.
        self.switch_player = True #True = premier joueur / False = deuxième joueur
        self.running = True # Controle la grande boucle de self.update
        self.combat = False # Verifie si on passe dans le combat ou non. 

        # Textes qui vont changer selon ou on se trouve dans le menu de selection des personnages. 
        self.desc = ["Bienvenue dans le sélecteur de","personnage.","","Vous n'avez pas encore","sélectionné de personnage.","","","","","",""]
        self.titre = "Joueur 1 : Choisissez un personnage !"
        self.texte = "Veuillez entrer votre nom :"
        self.texte_xy = [490, 75]

        # Attributs qui vont permettre d'enregistrer les personnages pour le combat. 
        self.nom_joueur = str()
        self.personnage = str()
        self.joueur1 = []
        self.joueur2 = []
        self.joueur = []

    @property
    def liste_personnages(self):
        UI[4].window_draw_rect(750,155,200,400)   

        for i in CTA:
            if CTA.index(i) > 4 :
                break
            self.Choix_Joueur = consoles[CTA.index(i)]
            i.ecrire(self.Choix_Joueur.nom, "Bold", 25, (770, CTA.index(i) * 80 + 175))
            i.surface = pygame.Rect(750, CTA.index(i) * 80 + 155, 175, 80)
            i.hover_check
            if i.cliquer:
                self.switch_selection = False
                self.personnage = i.texte
                self.perso_number = CTA.index(i) + 1
            pygame.draw.rect(jeu.screen, Blanc.RGB, (770, CTA.index(i) * 80 + 155, 160, 1))

    @property
    def accueil_perso(self):
        
        #Description
        UI[2].window_draw_rect(50, 200, 600, 275)
        x = 215
        for i in range(11):
            UI[2].ecrire(self.desc[i], "Medium", 23, (70,x))
            x += 30
        
        #Titre
        UI[3].window_draw_rect(50, 150, 600, 50) 
        UI[3].ecrire(self.titre, "Bold", 25, (70,160))

        CTA[5].disponible = False #Bouton de validation grise

    @property
    def infos_perso(self):
        #Remise a 0 des boutons perosnnages grise
        for i in range(5):
            CTA[i].disponible = True
        
        UI[1].window_draw_rect(50, 150, 200, 325) #Illustration
        
        #Description
        UI[2].window_draw_rect(250, 200, 400, 275)
        x = 215
        for i in range(3):
            UI[2].ecrire(self.desc[i], "Medium", 23, (270,x))
            x += 30
        
        #Titre
        UI[3].window_draw_rect(250, 150, 400, 50) 
        UI[3].ecrire(self.titre, "Bold", 25, (270,160))

        for i in range(5):
            if self.perso_number == i+1:
                self.Choix_Joueur = consoles[i]
                self.Choix_Joueur.dessiner_personnage(75,200,0)
                self.titre = self.Choix_Joueur.nom
                self.desc = self.Choix_Joueur.desc
                self.sante = f"{self.Choix_Joueur.sante}"
                CTA[i].disponible = False

        CTA[5].disponible = True #Bouton de validation non grise

    @property
    def validation(self):
        """ Code le bouton qui permet de valider son choix. """

        # Bouton de validation
        CTA[5].window_draw_rect(50,500,600,50)
        CTA[5].hover_check

        if self.switch_player:
            CTA[5].ecrire("Choix du deuxième personnage", "Bold", 25, (165, 510))

        else:
            CTA[5].ecrire("Lancement de la partie", "Bold", 25, (225, 510))

        if CTA[5].cliquer:

            if len(self.nom_joueur) < 3:
                CTA[5].couleur = Rouge.RGB
                self.texte = "Trop court !"
                self.texte_xy = [790,110]
                CTA[5].couleur = Blanc.RGB

            elif self.switch_player:
                self.switch_player = False
                self.texte = "Veuillez entrer votre nom :"
                self.texte_xy = [490, 75]
                self.desc = ["Bienvenue dans le sélecteur de","personnage.","","Vous n'avez pas encore","sélectionné de personnage.","","","","","",""]
                self.titre = "Joueur 2 : Choisissez un personnage !"

                # Enregistre les donnees du joueur 1 pour pouvoir l'utiliser dans le combat. 
                self.joueur1 = [] # Vide les donnees mis au prealable. 
                self.joueur1.append(self.nom_joueur)
                self.joueur1.append(1)
                self.joueur1.append(self.personnage)

                # Vide l'input pour pouvoir ecrire le nom du second joueur
                self.nom_joueur = str() 
                self.switch_selection = True
                for i in range(5):
                    CTA[i].disponible = True

            else:
                # Enregistre les donnees du joueur 1 pour pouvoir l'utiliser dans le combat. 
                self.joueur2.append(self.nom_joueur)
                self.joueur2.append(2)
                self.joueur2.append(self.personnage)

                self.running = False
                self.combat = True
                UI[0].transition_debut

    @property
    def input_pseudo(self):
        
        #Affiche le backgound et le rectangle ou on rentre le nom du personnage
        UI[5].window_draw_rect(750, 50, 200, 50)
        # UI[5].ecrire("_______","Regular",31, (790, 60))
        UI[5].ecrire("{}".format(self.nom_joueur),"Medium", 24, (795, 60))
        UI[5].ecrire(self.texte,"Medium",20, (self.texte_xy[0], self.texte_xy[1]))

        k = pygame.key.get_pressed()  

        clavier = [["A",K_a],["B",K_b],["C",K_c],["D",K_d],["E",K_e],["F",K_f],["G",K_g],["H",K_h],["I",K_i],["J",K_j],["K",K_k],["L",K_l],["M",K_m],["N",K_n],["O",K_o],["P",K_p],["Q",K_q],["R",K_r],["S",K_s],["T",K_t],["U",K_u],["V",K_v],["W",K_w],["X",K_x],["Y",K_y],["Z",K_z],["BACKSPACE",pygame.K_BACKSPACE]]

        if self.time_check:
            chrono_input.debut_timer
            for char, command in clavier:
                
                if k[command] and char == "BACKSPACE" and len(self.nom_joueur)>0:
                    self.nom_joueur = self.nom_joueur[:-1]
                elif k[command] and len(self.nom_joueur) < 7 and char != "BACKSPACE":
                    self.nom_joueur += char
            
    @property
    def bouton_retour(self):
        #Bouton de retour
        CTA[6].window_draw_rect(50, 50, 200, 50)
        CTA[6].hover_check
        CTA[6].ecrire("Retour", "Bold", 25, (110, 60))

        if CTA[6].cliquer:

            #Revenir au menu principal
            if self.switch_player is False:
                self.switch_player = True
                self.texte = "Veuillez entrer votre nom :"
                self.texte_xy = [490, 75]
                self.desc = ["Bienvenue dans le sélecteur de","personnage.","","Vous n'avez pas encore","sélectionné de personnage.","","","","","",""]
                self.titre = "Joueur 1 : Choisissez un personnage !"
                self.nom_joueur = str() 
                self.switch_selection = True
                for i in range(5):
                    CTA[i].disponible = True

            #Retour au menu principal
            else:
                self.running = False

    @property
    def time_check(self):
        """ Verifie s'il y a plus d'une seconde d'ecart entre nos clics. """

        chrono_input.update_time
        timer = chrono_input.temps_actuel - chrono_input.debut_compte

        # On peut cliquer qu'apres 0.4 sec par rapport au clic precedent. 
        if 70 - timer < 0:
            return True
        else :
            return False

    @property
    def update(self):
        """ Toutes les actions qui vont se derouler tant qu'on se trouve dans le menu de selection des personnages. """

        # Remet a 0 tous les attributs
        self.__init__()

        # Boucle qui tourne tant qu'on ne quitte pas ce menu de selection des personnages
        while self.running:

            # Charge le background et le lance sur l'ecran. 
            UI[0].background("BGai")

            # Permet de coder la croix pour quitter le jeu. 
            jeu.quit

            # Calcule la position de la souris 
            souris.pos_souris

            # Les deux types de choses qui sont affiches, selon ou on se trouve dans la selection des personnages
            if self.switch_selection:
                self.accueil_perso
            else:
                self.infos_perso  

            # Tous les objets de la page
            self.liste_personnages
            self.bouton_retour
            self.input_pseudo
            self.validation

            # Met a jour l'affichage de l'ecran.
            pygame.display.update()

            # Block le nombre de refreshrate a 60 fps.
            jeu.clock.tick(60)

#Initialisation du menu de selection de personnage
choix_personnage = Choix_Personnage()
