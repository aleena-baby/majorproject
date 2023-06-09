import cv2
import numpy as np
import os
import requests
import winsound

# Server URL
server_url = 'http://localhost:8080/alert'

def check_alert_status():
    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            alert_status = bool(int(response.text))
            return alert_status
        else:
            print('Failed to fetch alert status from the server.')
    except requests.exceptions.RequestException as e:
        print('Error connecting to the server:', e)
    return True

def play_alert_sound():
    if check_alert_status():
        duration = 1000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)

def recognize_face():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('Trainer_face_recognition/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize id counter
    id = 0
    count = 0

    # Read names from file
    with open('names.txt', 'r') as file:
        names = file.read().splitlines()

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # Set video width
    cam.set(4, 480)  # Set video height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=2,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            print(id)
            print(confidence)
            for nam in names:
                if nam.startswith(str(id)):
                    sd = nam

            print(sd)
            # confidence = round(100 - confidence)
            # Check if confidence is less than 100
            if confidence > 80 and id < len(names):
                ids = sd
            else:
                # print(names[id])
                ids = "unknown"
                count += 0.05

            # Check the alert status
            alert_status = check_alert_status()

            if alert_status and count > 1:
                cv2.putText(img, 'ALERT!', (x + 5, y + h + 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                play_alert_sound()
            elif not alert_status:
                count = 0

            cv2.putText(img, str(ids), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    recognize_face()
