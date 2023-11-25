import cv2 as cv
import numpy as np
 

#création d'un dictionnaire de marqueurs ArUco.
dico = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
 
# initialisation d'un détecteur de marqueurs
parametres =  cv.aruco.DetectorParameters_create()
 
# détection des marqueurs dans un cadre
coord_coins_marqueurs, mid_marqueurs, candidats_rejetes = cv.aruco.detectMarkers(fenetre, dico, parameters=parametres)
