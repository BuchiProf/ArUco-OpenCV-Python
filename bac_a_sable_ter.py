import cv2 as cv
import numpy as np
from icone import Icone
from kart import Kart
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



k1=Kart(1)
k2=Kart(2)
k3=Kart(3)
k4=Kart(4)
k2.has_banana = True
k1.has_banana = True

b1 = Icone('banane.png')
b2 = Icone('banane.png')
b3 = Icone('banane.png')
b4 = Icone('banane.png')
#c = Icone('champignon.png')
#ca = Icone('carapace.png')
#taille_image_banane = c.taille

def milieu_segment(A, B):
    x_A = int(A[0])
    y_A = int(A[1])
    x_B = int(B[0])
    y_B = int(B[1])
    x_M = int((x_A+x_B)/2.0)
    y_M = int((y_A+y_B)/2.0)
    return x_M, y_M

def coord_queue(A, B, C, D):
    """a partir des coordonnées des 4 coins du tag, on renvoie la coordonnées à l'arrière du kart"""
    #calcul du point milieu de AB
    E = milieu_segment(A, B)
    #calcul du point milieu de DC
    F = milieu_segment(D, C)
    #calcul du vecteur EF
    x_EF = F[0] - E[0]
    y_EF = F[1] - E[1]
    #coord de queue
    x_queue = int(F[0] + x_EF*1.5)
    y_queue = int(F[1] + y_EF*1.5)
    return x_queue, y_queue

def rayon_tag(A, C):
    """on calcul le rayon d'un tag"""
    diagonale = sqrt((int(A[0])-int(C[0]))**2 + (int(A[1])-int(C[1]))**2)
    return int(diagonale/2)

def position_kart(coins_marker, id_markers):
    """une fonction qui prend les marqueurs détéctés et met à jour les positions des karts"""
    for (markerCorner, markerID) in zip(coins_marker, id_markers):
                             
        coins = markerCorner.reshape((4, 2))
        #les coins A, B, C et D  sont respectivement  haut _gauche, haut _droite, bas_ droite, bas_ gauche      
        (point_A, point_B, point_C, point_D) = coins
        #print(coins)       
        rayon = rayon_tag(point_A, point_C)       
        #on centre sur le bas du tag
        kart_x ,kart_y = milieu_segment(point_C, point_D)
        
        if markerID[0] == 1:
            k1.x, k1.y = kart_x ,kart_y
            k1.rayon = int(rayon*1.3)
        if markerID[0] == 2:
            k2.x, k2.y = kart_x ,kart_y
            k2.rayon = int(rayon*1.3)
            k2.arriere_x, k2.arriere_y = coord_queue(point_A, point_B, point_C, point_D)
            cv.circle(img, coord_queue(point_A, point_B, point_C, point_D), 2, (255, 0, 0), 5)
        if markerID[0] == 3:
            k3.x, k3.y = kart_x ,kart_y
            k3.rayon = int(rayon*1.3)
        if markerID[0] == 4:
            k4.x, k4.y = kart_x ,kart_y
            k4.rayon = int(rayon*1.3)
        
###########################################################################
            #programme principal#
###########################################################################
while True:
    success, img = cap.read()
    # détection des markers avec renvoie des coins, des ids et des rejets
    coins_marker, id_markers, candidats_rejetes = detecteur.detectMarkers(img)
    #si on détecte quelque chose de valable
    if np.any(id_markers):
        #pour chaque couple de coins et son id trouvé dans l'ensemble détecté
        position_kart(coins_marker,id_markers)
    
    #cv.circle(img, (k1.x, k1.y), k1.rayon, (0, 0, 255), 1)
    cv.circle(img, (k2.x, k2.y), k2.rayon, (0, 0, 255), 1)
    #cv.circle(img, (k3.x, k3.y), k3.rayon, (0, 0, 255), 1)
    #cv.circle(img, (k4.x, k4.y), k4.rayon, (0, 0, 255), 1)
    
    if k1.has_banana:
        b1.afficher_icone_centre(img, k1.x, k1.y)
        
    if k2.has_banana:
        b2.afficher_icone_centre(img, k2.arriere_x, k2.arriere_y)
        
    if k3.has_banana:
        b3.afficher_icone_centre(img, k3.x, k3.y)
        
    if k4.has_banana:
        b4.afficher_icone_centre(img, k4.x, k4.y)
        
    img = cv.flip(img, 1)
    cv.imshow("Piste", img)
    #on appui sur 'd' pour lacher la banane de k1
    if cv.waitKey(1) & 0xFF == ord('d'):
        b1.dropped=True
        
    #un délai et l'événement touche 'q' enfoncée
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break

cv.destroyAllWindows()

