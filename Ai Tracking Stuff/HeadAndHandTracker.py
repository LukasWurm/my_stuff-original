import cv2 as cv
import numpy as np
import json
import csv
import copy
import argparse
import itertools
from collections import Counter, deque
import matplotlib.pyplot as plt
import mediapipe as mp

from utils import CvFpsCalc
from model import KeyPointClassifier, PointHistoryClassifier

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args

def show_live_image(img, ax, fig):
    """
    Update the displayed image in a live matplotlib window.
    
    Parameters:
        img: The image to display.
        ax: The matplotlib axes to update.
        fig: The matplotlib figure to update.
    """
    ax.clear()  # Clear previous image
    ax.axis('off')  # Hide axis
    if len(img.shape) == 2:  # If the image is grayscale
        ax.imshow(img, cmap='gray')
    else:  # If the image is in color
        ax.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    fig.canvas.draw()  # Update the figure
    plt.pause(0.001)  # Pause to allow matplotlib to update the figure

def main():
    # Argumente parsen
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    use_brect = True

    # Kamera vorbereiten
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # Mediapipe Handtracking initialisieren
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=4,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    keypoint_classifier = KeyPointClassifier()
    point_history_classifier = PointHistoryClassifier()

    # Labels lesen
    with open('model/keypoint_classifier/keypoint_classifier_label.csv',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]
    with open(
            'model/point_history_classifier/point_history_classifier_label.csv',
            encoding='utf-8-sig') as f:
        point_history_classifier_labels = csv.reader(f)
        point_history_classifier_labels = [
            row[0] for row in point_history_classifier_labels
        ]

    # FPS-Berechnung
    cvFpsCalc = CvFpsCalc(buffer_len=10)

    # Koordinatenhistorie
    history_length = 16
    point_history = deque(maxlen=history_length)

    # Fingergestenhistorie
    finger_gesture_history = deque(maxlen=history_length)

    mode = 0

    # Gesichtserkennung initialisieren
    recognizer = cv.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')

    face_cascade_Path = "haarcascade_frontalface_default.xml"
    faceCascade = cv.CascadeClassifier(face_cascade_Path)

    font = cv.FONT_HERSHEY_SIMPLEX

    names = ['None']
    with open('names.json', 'r') as fs:
        names = json.load(fs)
        names = list(names.values())

    # Matplotlib vorbereiten
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.ion()  # Interaktiver Modus
    fig.show()

    while True:
        fps = cvFpsCalc.get()

        # Tastendruck verarbeiten (ESC: Ende)
        key = cv.waitKey(10)
        if key == 27:  # ESC
            break
        number, mode = select_mode(key, mode)

        # Bild von der Kamera aufnehmen
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # Spiegelbildanzeige
        debug_image = copy.deepcopy(image)

        # Bild in Graustufen umwandeln für Gesichtserkennung
        gray = cv.cvtColor(debug_image, cv.COLOR_BGR2GRAY)

        # Gesichtserkennung
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(0.1 * cap_width), int(0.1 * cap_height)),
        )

        for (x, y, w, h) in faces:
            cv.rectangle(debug_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence > 51:
                try:
                    name = names[id]
                    confidence_text = "  {0}%".format(round(confidence))
                except IndexError:
                    name = "Who are you?"
                    confidence_text = "N/A"
            else:
                name = "Who are you?"
                confidence_text = "N/A"

            cv.putText(debug_image, name, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv.putText(debug_image, confidence_text, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        # Handtracking
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                pre_processed_point_history_list = pre_process_point_history(
                    debug_image, point_history)
                
                logging_csv(number, mode, pre_processed_landmark_list,
                            pre_processed_point_history_list)

                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                if hand_sign_id == 2:  # Point gesture
                    point_history.append(landmark_list[8])
                else:
                    point_history.append([0, 0])

                finger_gesture_id = 0
                point_history_len = len(pre_processed_point_history_list)
                if point_history_len == (history_length * 2):
                    finger_gesture_id = point_history_classifier(
                        pre_processed_point_history_list)

                finger_gesture_history.append(finger_gesture_id)
                most_common_fg_id = Counter(
                    finger_gesture_history).most_common()

                debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_info_text(
                    debug_image,
                    brect,
                    handedness,
                    keypoint_classifier_labels[hand_sign_id],
                    point_history_classifier_labels[most_common_fg_id[0][0]],
                )
        else:
            point_history.append([0, 0])

        debug_image = draw_point_history(debug_image, point_history)
        debug_image = draw_info(debug_image, fps, mode, number)

        # Aktualisiere das Live-Bild
        show_live_image(debug_image, ax, fig)

        # Überprüfe, ob das Fenster geschlossen wurde
        if not plt.fignum_exists(fig.number):
            break

    print("\n[INFO] Exiting Program.")
    cap.release()
    plt.ioff()  # Interaktiver Modus aus
    plt.close(fig)

# Hilfsfunktionen bleiben unverändert...
