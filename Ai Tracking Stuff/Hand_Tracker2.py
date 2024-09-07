import cv2
import numpy as np
import json
import csv
import copy
import argparse
import itertools
from collections import Counter, deque
from mediapipe import solutions as mp_solutions
import matplotlib.pyplot as plt
import mediapipe as mp
import os
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread

from utils import CvFpsCalc
from model import KeyPointClassifier, PointHistoryClassifier


# Initialisiere MediaPipe Hand Tracking Modul
mp_hands = mp_solutions.hands
mp_drawing = mp_solutions.drawing_utils

# Globale Variablen für die Konfiguration
max_num_hands = 2
min_detection_confidence = 0.7
min_tracking_confidence = 0.5

def draw_landmarks(image, landmarks, connections):
    if landmarks:
        h, w, c = image.shape
        for landmark in landmarks.landmark:
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)
        for connection in connections:
            start = connection[0]
            end = connection[1]
            x1, y1 = int(landmarks.landmark[start].x * w), int(landmarks.landmark[start].y * h)
            x2, y2 = int(landmarks.landmark[end].x * w), int(landmarks.landmark[end].y * h)
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return image

def draw_bounding_rect(image, brect):
    x, y, w, h = brect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

def draw_info_text(image, brect, handedness, hand_sign_text):
    x, y, _, _ = brect
    cv2.putText(image, f'Handedness: {handedness}', (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(image, f'Sign: {hand_sign_text}', (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return image

def calc_bounding_rect(image, landmarks):
    h, w, _ = image.shape
    x_min = int(min([lm.x for lm in landmarks.landmark]) * w)
    x_max = int(max([lm.x for lm in landmarks.landmark]) * w)
    y_min = int(min([lm.y for lm in landmarks.landmark]) * h)
    y_max = int(max([lm.y for lm in landmarks.landmark]) * h)
    return x_min, y_min, x_max - x_min, y_max - y_min

def logging_csv(number, mode, landmarks, point_history):
    file_name = 'hand_tracking_log.csv'
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'mode', 'number', 'landmarks']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    timestamp = time.time()
    landmark_list = [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, mode, number, landmark_list])

def show_live_image(img, ax, fig):
    ax.clear()
    ax.axis('off')
    if len(img.shape) == 2:
        ax.imshow(img, cmap='gray')
    else:
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    fig.canvas.draw()
    plt.pause(0.001)

def update_settings():
    global max_num_hands, min_detection_confidence, min_tracking_confidence
    max_num_hands = int(max_hands_entry.get())
    min_detection_confidence = float(min_detection_confidence_entry.get())
    min_tracking_confidence = float(min_tracking_confidence_entry.get())
    print(f"Updated settings: max_num_hands={max_num_hands}, min_detection_confidence={min_detection_confidence}, min_tracking_confidence={min_tracking_confidence}")

def start_camera():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    hands = mp_hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)
    
    # Matplotlib einrichten
    use_matplotlib = True
    if use_matplotlib:
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.ion()
        fig.show()

    mode = 0
    point_history = []

    while True:
        ret, img = cam.read()
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = hands.process(rgb_img)
        landmarks = results.multi_hand_landmarks[0] if results.multi_hand_landmarks else None
        handedness = results.multi_handedness[0].classification[0].label if results.multi_handedness else "Unknown"
        hand_sign_text = "Unknown"

        if landmarks:
            brect = calc_bounding_rect(img, landmarks)
            img = draw_bounding_rect(img, brect)
            img = draw_landmarks(img, landmarks, mp_hands.HAND_CONNECTIONS)
            img = draw_info_text(img, brect, handedness, hand_sign_text)

        img = cv2.flip(img, 1)

        if use_matplotlib:
            show_live_image(img, ax, fig)
        else:
            cv2.imshow('Hand Tracking', img)

        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break
        elif key == ord('1'):
            mode = 1
        elif key == ord('2'):
            mode = 2
        elif key == ord('0'):
            mode = 0
        elif mode == 1 and 48 <= key <= 57:
            number = key - 48
            logging_csv(number, mode, landmarks, point_history)
        elif mode == 2 and 48 <= key <= 57:
            number = key - 48
            logging_csv(number, mode, landmarks, point_history)

    print("\n[INFO] Exiting Program.")
    cam.release()
    if use_matplotlib:
        plt.ioff()
        plt.close(fig)
    cv2.destroyAllWindows()

# GUI-Einstellungen
def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Einstellungen")

    global max_hands_entry, min_detection_confidence_entry, min_tracking_confidence_entry

    tk.Label(settings_window, text="Maximale Anzahl der Hände:").grid(row=0, column=0, padx=10, pady=5)
    max_hands_entry = tk.Entry(settings_window)
    max_hands_entry.insert(0, str(max_num_hands))
    max_hands_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(settings_window, text="Minimale Erkennungsgenauigkeit:").grid(row=1, column=0, padx=10, pady=5)
    min_detection_confidence_entry = tk.Entry(settings_window)
    min_detection_confidence_entry.insert(0, str(min_detection_confidence))
    min_detection_confidence_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(settings_window, text="Minimale Verfolgungsgenauigkeit:").grid(row=2, column=0, padx=10, pady=5)
    min_tracking_confidence_entry = tk.Entry(settings_window)
    min_tracking_confidence_entry.insert(0, str(min_tracking_confidence))
    min_tracking_confidence_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(settings_window, text="Aktualisieren", command=update_settings).grid(row=3, column=0, columnspan=2, pady=10)

# Hauptfenster für die GUI
root = tk.Tk()
root.title("Hauptfenster")

tk.Button(root, text="Einstellungen öffnen", command=open_settings_window).pack(padx=20, pady=20)

# Startet den Kamerathread
camera_thread = Thread(target=start_camera, daemon=True)
camera_thread.start()

root.mainloop()
