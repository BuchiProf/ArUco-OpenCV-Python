import cv2 as cv
import numpy as np
from math import sqrt
#from icone import Icone

class Kart():
    def __init__(self, numero : int):
        """un Kart identifié par son id (de 1 à 4)"""
        self.id = numero
        self.has_banana = False
        self.x = 0
        self.y = 0
        self.rayon = 50
        self.arriere_x = 0
        self.arriere_y = 0
            