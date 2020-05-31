import cv2
from djitellopy import Tello
import numpy as np
import time
import math

drone = Tello()
drone.connect()
print(drone.get_battery())
try :
    drone.send_control_command("takeoff")
except:
    print('Takeoff bug')
drone.streamon()
time.sleep(3)
video = drone.get_frame_read()
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

x = False
y = False
z = False

drone.move_up(20)

while True:
    frame = cv2.cvtColor(video.frame, cv2.COLOR_BGR2BGRA)
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.25, minNeighbors=5)
    height, width = frame.shape[:2]
    centerframex = math.ceil(width/2)
    centerframey = math.ceil(height/2)
    frame = cv2.ellipse(frame, (centerframex, centerframey), (10, 10), 0, 0, 360, (0, 0, 255), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    key = cv2.waitKey(1)
    #Manual Controls:
        #-Disconnect and Shut Down
    if key == 27:
        drone.streamoff()
        cv2.destroyAllWindows()
        break
    try:
        if any(faces[0]):

            # y-axis-------------------------
            if (((2 * faces[0][1]) + faces[0][2])/2) + 150 > centerframey + 120:
                print('Down')
                drone.send_rc_control(0,0,-25,0)
                y = False
            if (((2 * faces [0][1]) + faces [0][2]) / 2) + 150 < centerframey - 120:
                print('Up')
                drone.send_rc_control(0,0,25,0)
                y = False
            # Y TRUE
            if (((2 * faces[0][1]) + faces[0][2])/2) + 150 <= centerframey + 120 and (((2 * faces [0][1]) + faces [0][2]) / 2) + 150 >= centerframey - 120:
                y = True

            # x-axis
            if ((2 * faces[0][0]) + faces[0][3])/2 > centerframex + 120 :
                print('Gauche')
                drone.send_rc_control(0,0,0,35)
                x = False
            if ((2 * faces[0][0]) + faces[0][3])/2 < centerframex - 120:
                print('Droite')
                drone.send_rc_control(0,0,0,-35)#was 35
                x = False
            # x true
            if ((2 * faces[0][0]) + faces[0][3])/2 <= centerframex + 120 and ((2 * faces[0][0]) + faces[0][3])/2 >= centerframex - 120:
                x = True

            # z - axis-----------------
            if faces[0][3] > 200:
                print("Près")
                drone.send_rc_control(0,-20,0,0)
                z = False
            if faces[0][3] < 120:
                print('Loin')
                drone.send_rc_control(0,20,0,0)
                z = False
            # Z TRUE
            if (faces[0][3]) <= 300 and (faces[0][3] >= 200):
                z = True
            
            if x == y == z == True:
                print('Centré')
                drone.send_rc_control(0,0,0,0)
        else:
            drone.send_rc_control(0,0,0,0)

    except IndexError:
        print('Pas de detection')
        pass
    for x, y, w, h in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
        centerx  = math.ceil((2 * x + w)/2)
        centery = math.ceil((2 * y + h)/2)
        frame = cv2.ellipse(frame, (centerx, (centery + 150)), (math.ceil(w * 0.05), math.ceil(h * 0.05)), 0, 0, 360, (0, 255, 0), 2)
        frame = cv2.arrowedLine(frame,(centerx, (centery + 150)), (math.ceil(width/2), math.ceil(height/2)), (255,0,0), 2)
    cv2.imshow('Tellotest', frame)
    cv2.moveWindow('Tellotest', 80, 40)

try:
    drone.land()
except:
    print('FINISH------')

