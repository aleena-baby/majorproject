import cv2
import os

def delete(n):
    with open('names.txt', 'r') as file:
        names = file.read().splitlines()
    folder_path = 'Dataset_face_recognition'
    files = os.listdir(folder_path)
    for name in names:
        idd=name[0:1]
        nam=name[2:]
        if nam==n:
            break
   


    for file in files:
        if file.startswith(f"User.{idd}."):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
    with open('names.txt', 'w') as file:
        for line in names:
            if not line.strip().startswith(f"{idd} "):
                file.write(line+"\n")


nam = input('Enter the person name: ')
delete(nam)