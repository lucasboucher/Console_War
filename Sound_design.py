# Les musiques et effets sonores du jeu. 

from pygame import mixer

class Son:
    """ Le sound design (effets sonores, musiques etc.)\nType : 1 = musique | 2 = SFX"""

    def __init__(self, Type): # Une fonction dans une classe s'appelle "une methode".

        self.musique = ["Principal_menu", "Arcade", "Port", "Victoire", "Match_nul"]
        self.SFX = ["Click", "Hover", "Hit1", "Hit2"]
        self.nom = str() 
        self.type = Type
        self.dico = {} # Dictionnaire qui enregistre tous les SFX et musiques du jeu

    @property
    def enregistre_son(self):
        """ Integre des elements dans le dictionnaire de musique et son. """
        if self.type == 1 :
            #Les musiques
            self.dico = {self.nom : "Assets/Sound_design/Musique/{}.wav".format(self.nom)}
        else :
            #Les sons
            self.dico = {self.nom : "Assets/Sound_design/SFX/{}.wav".format(self.nom)}
    
    def jouer(self, element, boucle):
        """ Boucle = -1 (tourne en boucle), 0 (ne tourne pas en boucle) \n\nLes muqiues disponibles :\n "Principal_menu", "Arcade", "Port", "Victoire", "Match_nul"\n\nLes SFX disponibles:\n "Click", "Hover", "Hit1", "Hit2" """

        self.nom = element
        self.enregistre_son

        if self.type == 1:
            # Si ce qu'on charge est une musique
            MUSIQUE = mixer.music.load(self.dico[self.nom]) # Permet de charger la musique dans une variable
            MUSIQUE = mixer.music.play(boucle) # Permet de la jouer en boucle
        else :
            # Si ce qu'on charge est un SFX
            SFX = mixer.Sound(self.dico[self.nom]) # Permet de charger le SFX dans une variable
            SFX.play() # Permet jouer le son

    @property
    def stop(self):
        """ Permet d'arreter la musique. """
        mixer.music.stop()
  
# Permet d'initialiser les musiques et sons du jeu.
musique = Son(1)
SFX = Son(2)