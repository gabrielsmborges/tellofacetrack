#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#Eviter que Kivy fasse des prints de debug sur la console
import os
#os.environ["KIVY_NO_CONSOLELOG"] = "1"
figlet = False
try:
    import pyfiglet
    figlet = True
except:
    pass
#Importer Kivy et ses modules necéssaires
import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from datetime import datetime
from time import sleep
#Importer la bibliothèque djitellopy (créée par Damia Fuentes)
from djitellopy import Tello
import numpy as np
from controller import command

if figlet:
    
    print('\033[44m-' * 80)
    print (f"\n\033[44m{pyfiglet.figlet_format('TelloFaceTrack')}")
    print('\033[44m-' * 80)


#Taille de la fenêtre (similaire à la taile de l'image du drone)
Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'resizable', False)

#Position de départ de la fenêtre


#Importer le HaarCascade (`Intelligence Artificielle`) qui detectera des  visages
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


#Variable qui va déterminer si le drone est en vol ou pas
drone_vol = False

compt_frames = 0

def connect():
    '''Connecter le drone'''
    return drone.connect()
    #print('Drone connecté')

def fluxvideo():
    return drone.get_frame_read().frame

def sendcommand(drone, face):
    command(drone, face)

class sManager(ScreenManager):
    pass

class ScreenOne(Screen):
    pass

class ScreenTwo(Screen):
    pass
        
class DroneImg(FloatLayout):
    def forever(self):
        """Fonction qui déclenchera l'accèes aux flux vidéo du drone"""
        #Créer un instance de Tello (djitellopy)
        #Maintenant drone aura toutes le propriétés données par le drone
        global drone
        drone = Tello()
        connect()
        fps = 1 / 24
        drone.streamon()
        Clock.schedule_interval(self.update, fps)
    def update(self, dt):
        #Capturer l'image
        frame = cv2.cvtColor(fluxvideo(), cv2.COLOR_BGR2BGRA)
        global compt_frames
        compt_frames += 1
        if compt_frames % 240 == 0:
            print(drone.get_battery())
        #print(frame.shape)
        frame = np.array(frame)
        #key = cv2.waitKey(int(100/24))
        #Sauvegarder une copie du fram afin de l'enregistrer au cas ou l'utilisateur veut sauvegarder la photo
        global im
        im = frame.copy()
        #cv2.imshow('ezf', photo_frame)
        """
            La variable grayframe sert a transformer l'image capturée en noir et blanc qui est 3x moins lourde
            que l'image rgb, de plus on diminue sa taille en 4 fois. Ce qui à analyser des visges sur une image 12x moins lourde que l'originale (frame)
        """
        grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('edf', grayframe)
        grayframe = cv2.resize(grayframe, (int(grayframe.shape[1]/4), int(grayframe.shape[0]/4)))
        #Detection de visages sur l'image grayframe
        faces = np.array(face_cascade.detectMultiScale(grayframe, scaleFactor=1.1, minNeighbors=4))
        for x, y, w, h in faces:
            x, y, w, h = x * 4, y * 4, w * 4, h * 4
            #Dessiner carré sur le visage
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 5)
        try:
            sendcommand(drone, faces * 4)
        except:
            pass
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (frame.shape[1]*2, frame.shape[0]*2))
        buf1 = cv2.flip(frame, 0)
        buf = buf1.flatten()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgra')
        texture1.blit_buffer(buf, colorfmt='bgra', bufferfmt='ubyte')
        # affecter a la texture de l'image de l'interface graphique l'image qu'on a cqpturé
        self.ids.my_img.texture = texture1

    def take_photo(self):
        #Acquérir la date actuelle
        date = datetime.now()
        #Crér un nom personalisé pour ma photo avec la date
        date = date.strftime("%Y-%m-%d_%H-%M-%S")
        #Sauvegarder la photo sur le dossier gallerie avec le nom personalisé
        cv2.imwrite(f'gallerie/{date}.jpeg', im, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

    def takeoff(self):
        print('Décollage')
        try:
            drone.takeoff()
            drone_vol = True
        except:
            print('Erreur de décollage')
            
    
    def land(self):
        print('Attérissage')
        try:
            drone.land()
            drone_vol = False
        except:
            print('Erreur d\'atterissage')

class CamPage(Screen):
    pass

class TestApp(App):
    def build(self):
        Window.top = 30
        Window.left = 0
        self.icon = "assets/ailesrgb.png"
        return sManager()
    def on_stop(self):
        if 'drone' in globals():
            drone.land()
            drone.streamoff()
        cv2.destroyAllWindows()
    def on_resize(self, w, h):
        print('Resizing')


if __name__ == '__main__':
    TestApp.title = "TelloFaceTrack"
    TestApp().run()
