import numpy as np
import cv2
import pickle
import pyttsx3
import win32gui, win32con

import argparse
import imutils
import subprocess

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# load time variables
def my_time():
    global a
    global b
    from datetime import datetime
    from datetime import time
    import datetime
    datetime_object = datetime.datetime.now()
    a = time(datetime_object.hour,datetime_object.minute)
    b = time(12,00,00)

# load speech engine
def my_speak(message):
    engine = pyttsx3.init()
    engine.say('{}'.format(message))
    engine.runAndWait()

# speech output definition
message = ("Hallo Christoph viel Spaas heute")
message2 = ("Hallo Gabriela viel Spaas heute")
minimizewindow = 1

# load cv2 classifier
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

# initialize the first frame in the video stream for motion detection
firstFrame = None

# initialize trained model and video capture
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

# start programm
while(cap.isOpened()):
    #read time
    my_time()

    ##FACE DETECTION
    #Capture frame-by-frame
    ret, frame = cap.read()
    text = "Unoccupied" 
    if ret == True:
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            #print(x,y,w,h)
            roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]

            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf>=4 and conf <= 85:
                #print(5: #id_)
                #print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

            ##SPEECH OUTPUT
            if name == ("christoph") and b > a:
                import time
                my_speak(message)
                time.sleep(5)
                if name == ("gabriela"):
                    my_speak(message2)
                    time.sleep(5)
                time.sleep(30)

            if name == ("gabriela") and b > a:
                import time
                my_speak(message2)
                time.sleep(5)
                if name == ("christoph"):
                    my_speak(message)
                    time.sleep(5)
                time.sleep(30)

            img_item = "7.png"
            cv2.imwrite(img_item, roi_color)

            color = (255, 0, 0) #BGR 0-255 
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

    ## MOTION DETECTION:
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 80, 255, cv2.THRESH_BINARY)[1]
     
        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=1)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
     
        # loop over the contours
        for c in cnts:
            if cv2.contourArea(c) < args["min_area"]: # if the contour is too small, ignore it
                text = "Unoccupied"
                firstFrame = gray
            else:
                text = "Occupied"
                subprocess.call("cscript ENTER.vbs")
                firstFrame = gray

        # draw the text and timestamp on the frame
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    ## DISPLAY FRAME AND MINIMIZE WINDOW

        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

        Minimize = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
        
    else:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
