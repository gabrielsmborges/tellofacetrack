import cv2
from djitellopy import Tello
import numpy as np
import time
import math



""" Variables qui déterminent si le visage est centré et avec une bonne distance
On initialise par False et l'algorithme va ensuite determiner si les cordonnées sont bonnes"""
x = False
y = False
z = False

height, width = 720, 960
centerframex = math.ceil(width/2)
centerframey = math.ceil(height/2)

def sendcommand(face):
    #Taille de l'image donée par le drone 
    try:
        if any(face[0]):

            # y-axis-------------------------
            if (((2 * face[0][1]) + face[0][2])/2) + 150 > centerframey + 120:
                print('Down')
                drone.send_rc_control(0,0,-25,0)
                y = False
            if (((2 * face [0][1]) + face [0][2]) / 2) + 150 < centerframey - 120:
                print('Up')
                drone.send_rc_control(0,0,25,0)
                y = False
            # Y TRUE
            if (((2 * face[0][1]) + face[0][2])/2) + 150 <= centerframey + 120 and (((2 * face [0][1]) + face [0][2]) / 2) + 150 >= centerframey - 120:
                y = True

            # x-axis
            if ((2 * face[0][0]) + face[0][3])/2 > centerframex + 120 :
                print('Gauche')
                drone.send_rc_control(0,0,0,35)
                x = False
            if ((2 * face[0][0]) + face[0][3])/2 < centerframex - 120:
                print('Droite')
                drone.send_rc_control(0,0,0,-35)#was 35
                x = False
            # x true
            if ((2 * face[0][0]) + face[0][3])/2 <= centerframex + 120 and ((2 * face[0][0]) + face[0][3])/2 >= centerframex - 120:
                x = True

            # z - axis-----------------
            if face[0][3] > 200:
                print("Près")
                drone.send_rc_control(0,-20,0,0)
                z = False
            if face[0][3] < 120:
                print('Loin')
                drone.send_rc_control(0,20,0,0)
                z = False
            # Z TRUE
            if (face[0][3]) <= 300 and (face[0][3] >= 200):
                z = True
            
            if x == y == z == True:
                print('Centré')
                drone.send_rc_control(0,0,0,0)
        else:
            drone.send_rc_control(0,0,0,0)

    except IndexError:
        print('Pas de detection')
        pass

if __name__ = "__main__":
    print("Cet algorithme n'est pas fait pour être éxécuté directement, veuillez l'importer sur un autre fichier")