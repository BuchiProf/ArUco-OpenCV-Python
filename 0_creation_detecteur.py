import cv2 as cv
import numpy as np
 

#création d'un dictionnaire de marqueurs ArUco.
dico = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)
 
# initialisation des paramètres d'un détecteur de marqueurs
parametres =  cv.aruco.DetectorParameters()

#création du détecteur
detecteur = cv.aruco.ArucoDetector(dico, parametres)

# charger une image avec 'IMREAD'
img = cv.imread("6markers_test.png")

# détection des markers avec renvoie des coins, des ids et des rejets
coord_coins_marker, id_marker, candidats_rejetes = detecteur.detectMarkers(img)

#la fonction qui dessine les contours
cv.aruco.drawDetectedMarkers(img, coord_coins_marker, id_marker,(0, 0, 255))

# on affiche le resultat
cv.imshow("6markers_test.png", img)

#waitKey indique la durée d'affichage de l'image en ms
#si la valeur est "0" alors elle ne ferme pas
cv.waitKey(0)