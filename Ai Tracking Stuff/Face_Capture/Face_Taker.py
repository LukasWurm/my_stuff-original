import numpy as np
import json
import cv2
import os
from PIL import Image
import time
import matplotlib.pyplot as plt

def create_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_face_id(directory: str) -> int:
    user_ids = []
    for filename in os.listdir(directory):
        number = int(os.path.split(filename)[-1].split("-")[1])
        user_ids.append(number)
    user_ids = sorted(list(set(user_ids)))
    max_user_ids = 1 if len(user_ids) == 0 else max(user_ids) + 1
    for i in sorted(range(0, max_user_ids)):
        try:
            if user_ids.index(i):
                face_id = i
        except ValueError as e:
            return i
    return max_user_ids

def save_name(face_id: int, face_name: str, filename: str) -> None:
    names_json = None
    if os.path.exists(filename):
        with open(filename, 'r') as fs:
            names_json = json.load(fs)
    if names_json is None:
        names_json = {}
    names_json[face_id] = face_name
    with open(filename, 'w') as fs:
        json_dump = json.dumps(names_json, ensure_ascii=False, indent=4)
        fs.write(json_dump)

def show_image(img, title='Image'):
    """
    Display an image using matplotlib.

    Parameters:
        img: The image to display.
        title: The title of the image window.
    """
    plt.figure(figsize=(10, 6))
    if len(img.shape) == 2:  # If the image is grayscale
        plt.imshow(img, cmap='gray')
    else:  # If the image is in color
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')  # Hide axis
    plt.show()

if __name__ == '__main__':
    directory = 'images'
    cascade_classifier_filename = 'haarcascade_frontalface_default.xml'
    names_json_filename = 'names.json'

    create_directory(directory)
    faceCascade = cv2.CascadeClassifier(cascade_classifier_filename)
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    count = 0
    face_name = input('\nEnter user name and press <return> -->  ')
    face_id = get_face_id(directory)
    save_name(face_id, face_name, names_json_filename)
    print('\n[INFO] Initializing face capture. Look at the camera and wait...')

    while True:
        ret, img = cam.read()
        if not ret or img is None:
            print("Fehler: Kein Bild von der Kamera erhalten.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite(f'./images/Users-{face_id}-{count}.jpg', gray[y:y+h, x:x+w])

        # Zeige das Bild ohne GUI, nur in Jupyter-Umgebungen oder in einer statischen Umgebung
        show_image(img, title=f'Captured Image {count}')

        time.sleep(0.1)

        # change the number to the desired number of images to be captured

        if count >= 40:
            break

    print('\n[INFO] Success! Exiting Program.')
    cam.release()
