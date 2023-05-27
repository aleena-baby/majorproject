import cv2
import os

def addDataset():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # For each person, enter one numeric face id
    face_id = input('\n enter user id and press <return> ==>  ')
    face_name = input("\n Enter user name")

    print("\n [INFO] Initializing face capture. Look at the camera and wait ...")
    # Initialize individual sampling face count
    count = 0

    # Find the next available image number
    existing_images = os.listdir("Dataset_face_recognition")
    existing_ids = [int(file.split('.')[1]) for file in existing_images if file.split('.')[0] == "User"]
    if existing_ids:
        count = max(existing_ids) + 1

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            count += 1
            roi_color = img[y:y+h,x:x+w]
            cv2.imshow("temp",roi_color)
            # Save the captured image into the datasets folder
            cv2.imwrite("Dataset_face_recognition/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])

            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27 or count >= 100: # Take 30 face samples or press 'ESC' to stop
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

    # Call the training code only if new images were added
    if count > 0:
        os.system("python 02_face_training.py")

    # Update the names array in face recognition code
    with open('names.txt', 'a') as file:
        file.write(face_id+" "+face_name+"\n")

# Usage example
# choice=input("do you want to add a user or delete")
# if choice=="add":
addDataset()
#elif choice=="delete":
 #   nam = input('Enter the person name: ')
  #  delete(nam)
#else:
 #   print("error")

