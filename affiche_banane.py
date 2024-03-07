import cv2 as cv
import numpy as np
from math import sqrt

cap = cv.VideoCapture(0)
largeur  = cap.get(cv.CAP_PROP_FRAME_WIDTH )
hauteur = cap.get(cv.CAP_PROP_FRAME_HEIGHT )
#définition du dictionnaire de markers
dico = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)
#création des parametres du détecteur
parametres =  cv.aruco.DetectorParameters()
#création du détecteur
detecteur = cv.aruco.ArucoDetector(dico, parametres)
banane = cv.imread('banane.png')
taille_image_banane = 50
banane = cv.resize(banane, (taille_image_banane, taille_image_banane)) 
# Create a masque of banane 
img2gray = cv.cvtColor(banane, cv.COLOR_BGR2GRAY) 
ret, masque = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY) 

print(banane.shape)



while True:
    success, img = cap.read()
    
    
# détection des markers avec renvoie des coins, des ids et des rejets
    coins_marker, id_marker, candidats_rejetes = detecteur.detectMarkers(img)
###########################################################################
    if np.any(id_marker):
        for (markerCorner, markerID) in zip(coins_marker, id_marker):
                coins_marker = markerCorner.reshape((4, 2))
                (haut_gauche, haut_droite, bas_droite, bas_gauche) = coins_marker

                haut_droite = (int(haut_droite[0]), int(haut_droite[1]))
                bas_droite = (int(bas_droite[0]), int(bas_droite[1]))
                bas_gauche = (int(bas_gauche[0]), int(bas_gauche[1]))
                haut_gauche = (int(haut_gauche[0]), int(haut_gauche[1]))
                diagonale = sqrt((haut_gauche[0]-bas_droite[0])**2 + (haut_gauche[1]-bas_droite[1])**2)
                rayon = int(diagonale/2)
                cX = int((haut_gauche[0] + bas_droite[0]) / 2.0)
                cY = int((haut_gauche[1] + bas_droite[1]) / 2.0)
                cv.circle(img, (cX, cY), rayon, (0, 0, 255), 5)
                
                zone_masque = img[cY-taille_image_banane//2:taille_image_banane//2+cY,
                                  cX-taille_image_banane//2:taille_image_banane//2+cX]
                
  
                # affichage de la banane 
                x,y,c = np.shape(zone_masque)
                if x == taille_image_banane and y == taille_image_banane:
                    zone_masque[np.where(masque)] = 0
                    zone_masque += banane 

    
#########################################################################
#la fonction qui dessine les contours
    #cv.aruco.drawDetectedMarkers(img, coins_marker,id_marker)
    
  

    cv.imshow("Resultat", img)
    #un délai et l'événement touche 'q' enfoncée

    img = cv.flip(img, 1)
    if cv.waitKey(10) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break





