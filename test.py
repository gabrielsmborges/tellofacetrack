from djitellopy import Tello
import cv2
from time import sleep

drone = Tello()
drone.connect()
drone.streamon()
sleep(3)
video = drone.get_frame_read()

while True:
    cv2.imshow('Tellotest', video.frame)
    key = cv2.waitKey(int(1000/24))
    