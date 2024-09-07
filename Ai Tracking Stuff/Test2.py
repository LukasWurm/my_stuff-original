import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
import json
import tkinter as tk
from tkinter import ttk

# Gesichtserkennung und -erkennung initialisieren
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

# Namen aus der JSON-Datei laden
with open('names.json', 'r') as file:
    names = json.load(file)

# Warnungen und Logs unterdrücken
tf.get_logger().setLevel('ERROR')

# Mediapipe initialisieren
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# GPU verwenden, wenn verfügbar
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
    except RuntimeError as e:
        print(e)

# TKinter-Fenster erstellen
root = tk.Tk()
root.title("Settings")
root.geometry("300x400")

# Schieberegler für min Face confidence
min_face_confidence_label = tk.Label(root, text="Min Face Confidence")
min_face_confidence_label.pack()
min_face_confidence = tk.DoubleVar(value=0.5)
min_face_confidence_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, variable=min_face_confidence)
min_face_confidence_slider.pack()

# Schieberegler für min Hand detection confidence
min_hand_confidence_label = tk.Label(root, text="Min Hand Detection Confidence")
min_hand_confidence_label.pack()
min_hand_confidence = tk.DoubleVar(value=0.5)
min_hand_confidence_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, variable=min_hand_confidence)
min_hand_confidence_slider.pack()

# Checkbox für FPS-Anzeige
show_avg_fps = tk.BooleanVar()
avg_fps_check = tk.Checkbutton(root, text="Show Average FPS", variable=show_avg_fps)
avg_fps_check.pack()

# Funktion zum Aktualisieren des FPS-Anzeige-Fensters
def update_fps_display():
    if show_avg_fps.get():
        fps_label.pack()
    else:
        fps_label.pack_forget()

# FPS-Fenster erstellen
fps_window = tk.Toplevel(root)
fps_window.title("FPS")
fps_window.geometry("300x100")
fps_label = tk.Label(fps_window, text="FPS: 0.0")
fps_label.pack()

# Webcam-Feed starten
cap = cv2.VideoCapture(0)
fps_values = []

with mp_hands.Hands(
    min_detection_confidence=min_hand_confidence.get(),
    min_tracking_confidence=min_hand_confidence.get()) as hands:

    def update_frame():
        ret, frame = cap.read()
        if not ret:
            print("Ignoriere leeren Frame.")
            return

        # Gesichtserkennung
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            face_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if confidence < (1 - min_face_confidence.get()) * 100:
                confidence_text = f"{round(100 - confidence, 2)}%"
                name = names.get(str(face_id), "Unknown")
                cv2.putText(frame, name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, confidence_text, (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Handerkennung
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # FPS berechnen
        fps = cap.get(cv2.CAP_PROP_FPS)
        fps_values.append(fps)
        if len(fps_values) > 30:
            fps_values.pop(0)
        avg_fps = sum(fps_values) / len(fps_values)

        # FPS-Anzeige aktualisieren
        fps_label.config(text=f"FPS: {fps:.2f}")
        if show_avg_fps.get():
            fps_label.config(text=f"FPS: {fps:.2f} | Avg FPS: {avg_fps:.2f}")
        else:
            fps_label.config(text=f"FPS: {fps:.2f}")

        cv2.imshow('Hand and Face Detection', frame)

        # Fenster dynamisch anpassen
        root.after(10, update_frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC zum Beenden
            cap.release()
            cv2.destroyAllWindows()
            root.quit()

    update_frame()
    root.mainloop()
