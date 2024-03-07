from math import sqrt
import cv2 as cv
import numpy as np

class Icone:
    def __init__(self, fichier_image : str):
        """construit une icone avec : - une image en png pour la transparence - une coordonnée en x et y par défaut en haut à gauche - la taille par défaut de l'image en pixel"""
        self.x = 0
        self.y = 0
        self.taille = 50
        self.image = cv.imread(fichier_image)
        # on reduit la taille de l'image
        self.image = cv.resize(self.image, (self.taille, self.taille))
    
    def create_mask(self):
        """création d'un masque pour la transparence des bord"""
        img2gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY) 
        ret, masque = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY)
        return masque
        
    def afficher_icone(self, fenetre, x, y):
        """affichage de l'icone dans la fenetre aux coordonnées x et y"""
        masque = self.create_mask()
        # on affiche une banane
        zone_masque = fenetre[x:self.taille+x, y:self.taille+y]
        zone_masque[np.where(masque)] = 0
        zone_masque += self.image
        
def distance(a:tuple, b:tuple) -> float:
    """calcul une distance entre deux points"""
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
