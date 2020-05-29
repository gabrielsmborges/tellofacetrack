#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#Eviter que Kivy fasse des prints de debug sur la console
import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

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

Window.size = (1280, 720)
Window.top, Window.left = 30, 0
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


class sManager(ScreenManager):
    pass

class ScreenOne(Screen):
    pass

class ScreenTwo(Screen):
    pass
        
class DroneImg(FloatLayout):
    def forever(self):
        self.capture = cv2.VideoCapture(0)
        fps = 1 / 24
        Clock.schedule_interval(self.update, fps)
    def update(self, dt):
        #Capturer l'image
        ret, frame = self.capture.read()
        global im
        im = frame.copy()
        #Sauvegarder une copie du fram afin de l'enregistrer au cas ou l'utilisateur veut sauvegarder la photo

        #cv2.imshow('ezf', photo_frame)
        """
            La variable grayframe sert a transformer l'image capturée en noir et blanc qui est 3x moins lourde
            que l'image rgb, de plus on diminue sa taille en 3 fois. Ce qui à analyser des visges sur une image 9x moins lourde que l'originale (frame)
        """
        grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayframe = cv2.resize(grayframe, (int(grayframe.shape[1]/4), int(grayframe.shape[0]/4)))

        #Detection de visages sur l'image grayframe
        faces = face_cascade.detectMultiScale(grayframe, scaleFactor=1.25, minNeighbors=5)
        for x, y, w, h in faces:
            x, y, w, h = x*4, y*4, w*4, h*4

            #Dessiner carré sur le visage
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
        
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (frame.shape[1] * 2, frame.shape[0] * 2))
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.ids.my_img.texture = texture1

    def take_photo(self):
        #Acquérir la date actuelle
        date = datetime.now()
        #Crér un nom personalisé pour ma photo avec la date
        date = date.strftime("%Y-%m-%d_%H-%M-%S")
        #Sauvegarder la photo sur le dossier gallerie avec le nom personalisé
        cv2.imwrite(f'gallerie/{date}.png', im)
   
class CamPage(Screen):
    def take_photo(self):
        DroneImg().take_photo()
    pass


class TestApp(App):
    def build(self):
        return sManager()




if __name__ == '__main__':
    TestApp.title = "TelloFaceTrack"
    TestApp().run()
