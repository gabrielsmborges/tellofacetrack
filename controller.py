"""
Ce programme reçoit les coordonnées du visage envoyées par le programme principal et envoie des commandes vers le drone.
Ainsi le drone va constamment essyer de se positionner afin que l'utilisateur soit toujours centré dans le frame
"""

import numpy as np
import time
import math
#threading servira à executer les fonctions d'alignement en même temps
from threading import Thread


""" Variables qui déterminent si le visage est centré et avec une bonne distance
On initialise par False et l'algorithme va ensuite determiner si les cordonnées sont bonnes"""
x = False
y = False
z = False

height, width = 720, 960
centerframex = math.ceil(width/2)
centerframey = math.ceil(height/2)


def align_x(drone, face):
    # Coordonnées X
        if ((2 * face[0][0]) + face[0][3])/2 > centerframex + 120 :
            #print('Gauche')
            drone.send_rc_control(0,0,0,35)
            x = False
        if ((2 * face[0][0]) + face[0][3])/2 < centerframex - 120:
            #print('Droite')
            drone.send_rc_control(0,0,0,-35)
            x = False
        # X True i.e Visage centré horizontalement
        else: #((2 * face[0][0]) + face[0][3])/2 <= centerframex + 120 and ((2 * face[0][0]) + face[0][3])/2 >= centerframex - 120:
            x = True

def align_y(drone, face):
    # Coordonnées Y
    if (((2 * face[0][1]) + face[0][2])/2) + 150 > centerframey:
        #print('Down')
        drone.send_rc_control(0,0,-25,0)
        y = False
    if (((2 * face [0][1]) + face [0][2]) / 2) + 150 < centerframey:
        #print('Up')
        drone.send_rc_control(0,0,25,0)
        y = False
    # Y TRUE i.e Visage centré verticalement
    else: #(((2 * face[0][1]) + face[0][2])/2) + 150 <= centerframey + 120 and (((2 * face [0][1]) + face [0][2]) / 2) + 150 >= centerframey - 120:
            y = True

def align_z(drone, face):
    # Coordonées Z
    if face[0][3] > 200:
        #print("Près")
        drone.send_rc_control(0,-20,0,0)
        z = False
    if face[0][3] < 120:
        #print('Loin')
        drone.send_rc_control(0,20,0,0)
        z = False
    # Z TRUE i.e Bonne distance de l'utilisateur
    else: #(face[0][3]) <= 300 and (face[0][3] >= 200):
            z = True
    
def command(drone, face):
    """
        Reçoit les coordonnées et les renvoie vers le drone
    """
    #Taille de l'image donée par le drone 
    try:
        #Si il y a un visage dans le frame
        if face.size > 0:
            if x == y == z == True:
                #Si le visage est centré envoyer une commande nulle au drone
                #print('Centré')
                drone.send_rc_control(0,0,0,0)
            else:
                Thread(target = align_x, args = (drone, face)).start()
                Thread(target = align_y, args = (drone, face)).start()
                Thread(target = align_z, args = (drone, face)).start()
        else:
            #S'il ny a pas de visages détectés, envoyer des commandes nulles au drone
            drone.send_rc_control(0,0,0,0)

    except IndexError:
        print('Le programme n\'a pas réussi à envoyer des commandes au drone')
        pass

if __name__ == "__main__":
    """Si la personne execute ce fixhier directement; le programme renvoie un message d'erreur"""
    print("\n\n\033[91m\033[1mCet algorithme n'est pas fait pour être éxécuté directement, veuillez l'importer sur un autre fichier.\n\n")