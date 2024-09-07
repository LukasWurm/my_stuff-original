import cv2
import mediapipe as mp
import tensorflow as tf
import numpy as np
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

# GPU Check
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Initialisieren der Mediapipe-Komponenten für Hand- und Gesichtserkennung
mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)

# Globale Variablen
hand_tracking_mode = 2
hand_confidence = 0.7
face_confidence = 0.7
fps = 0
avg_fps = 0
fps_count = 0
fps_sum = 0
exit_event = False
show_avg_fps = False

# FPS Zähler
last_time = time.time()

# Funktionen zur Hand- und Gesichtserkennung
def process_frame(frame):
    global last_time, fps, avg_fps, fps_count, fps_sum
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Hand-Erkennung
    results_hands = hands.process(image_rgb)
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks[:hand_tracking_mode]:
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Gesichtserkennung
    results_face = face_detection.process(image_rgb)
    if results_face.detections:
        for detection in results_face.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{detection.score[0]:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # FPS Berechnung
    current_time = time.time()
    fps = int(1 / (current_time - last_time))
    last_time = current_time
    
    # Durchschnittliche FPS Berechnung
    fps_count += 1
    fps_sum += fps
    avg_fps = fps_sum / fps_count
    
    return frame

def video_stream():
    global exit_event
    cap = cv2.VideoCapture(0)
    
    while not exit_event:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = process_frame(frame)
        
        cv2.imshow('Hand and Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            exit_event = True
    
    cap.release()
    cv2.destroyAllWindows()

# GUI-Funktionen
def update_hand_tracking_mode(value):
    global hand_tracking_mode
    hand_tracking_mode = int(float(value))
    hand_tracking_label.config(text=f"Max Hand Render: {hand_tracking_mode}")

def update_confidence(value, confidence_type):
    global hand_confidence, face_confidence
    if confidence_type == 'hand':
        hand_confidence = float(value)
    elif confidence_type == 'face':
        face_confidence = float(value)

def toggle_avg_fps():
    global show_avg_fps
    show_avg_fps = avg_fps_var.get()
    update_fps_display()

def update_fps():
    global fps_label, avg_fps_label
    fps_label.config(text=f"FPS: {fps}")
    if show_avg_fps:
        avg_fps_label.config(text=f"Avg FPS: {avg_fps:.2f}")
    else:
        avg_fps_label.config(text="")

def update_fps_display():
    global fps_label, avg_fps_label, fps_window
    if show_avg_fps:
        avg_fps_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    else:
        avg_fps_label.grid_forget()  # Entfernt die Anzeige, wenn deaktiviert
    
    # Die Position der Labels wird neu angepasst, wenn die Fenstergröße sich ändert
    adjust_label_font(fps_label, fps_window)
    adjust_label_font(avg_fps_label, fps_window)
    fps_window.update_idletasks()  # Erzwingt ein Update der GUI
    fps_label.update_idletasks()
    avg_fps_label.update_idletasks()

def adjust_label_font(label, window):
    """Stellt die Schriftgröße basierend auf der Fenstergröße ein"""
    font_size = int(window.winfo_height() / 20)  # Schriftgröße proportional zur Fensterhöhe
    label.config(font=("Arial", font_size))

def run_settings_window():
    global hand_tracking_label, fps_label
    global avg_fps_checkbox, avg_fps_var, exit_event

    settings_window = tk.Tk()
    settings_window.title("Settings")
    settings_window.geometry("400x400")  # Initialgröße
    
    settings_window.grid_columnconfigure(0, weight=1)
    settings_window.grid_rowconfigure(0, weight=1)
    settings_window.grid_rowconfigure(1, weight=1)
    settings_window.grid_rowconfigure(2, weight=1)
    settings_window.grid_rowconfigure(3, weight=1)
    settings_window.grid_rowconfigure(4, weight=1)
    settings_window.grid_rowconfigure(5, weight=1)
    settings_window.grid_rowconfigure(6, weight=1)

    # Hand Tracking
    hand_tracking_label = tk.Label(settings_window, text=f"Max Hand Render: {hand_tracking_mode}")
    hand_tracking_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    hand_tracking_slider = tk.Scale(settings_window, from_=1, to=10, orient=tk.HORIZONTAL, command=update_hand_tracking_mode)
    hand_tracking_slider.set(hand_tracking_mode)
    hand_tracking_slider.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    
    # Confidence
    tk.Label(settings_window, text="Hand Confidence:").grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    hand_confidence_slider = tk.Scale(settings_window, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, command=lambda value: update_confidence(value, 'hand'))
    hand_confidence_slider.set(hand_confidence)
    hand_confidence_slider.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(settings_window, text="Face Confidence:").grid(row=4, column=0, padx=10, pady=10, sticky="ew")
    face_confidence_slider = tk.Scale(settings_window, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, command=lambda value: update_confidence(value, 'face'))
    face_confidence_slider.set(face_confidence)
    face_confidence_slider.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    # Durchschnittliche FPS Checkbox
    avg_fps_var = tk.BooleanVar()
    avg_fps_checkbox = tk.Checkbutton(settings_window, text="Show Avg FPS", variable=avg_fps_var, command=toggle_avg_fps)
    avg_fps_checkbox.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    # Handler für das Schließen des Settings-Fensters
    def on_closing():
        global exit_event
        exit_event = True
        settings_window.destroy()

    settings_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Starten des GUI
    settings_window.mainloop()

def run_fps_window():
    global fps_label, avg_fps_label, exit_event
    global fps_window

    fps_window = tk.Tk()
    fps_window.title("FPS Display")
    fps_window.geometry("400x200")  # Initialgröße

    fps_window.grid_columnconfigure(0, weight=1)
    fps_window.grid_rowconfigure(0, weight=1)
    fps_window.grid_rowconfigure(1, weight=1)

    fps_label = tk.Label(fps_window, text=f"FPS: {fps}")
    fps_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    avg_fps_label = tk.Label(fps_window, text="")
    avg_fps_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def update_fps_display_loop():
        while not exit_event:
            update_fps()
            time.sleep(1 / update_interval)

    # Update-Intervall in Sekunden
    update_interval = 1

    # Starten eines Threads für das Update der FPS-Anzeige
    fps_thread = Thread(target=update_fps_display_loop)
    fps_thread.start()

    # Handler für das Schließen des FPS-Fensters
    def on_closing():
        global exit_event
        exit_event = True
        fps_window.destroy()

    fps_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Starten des GUI
    fps_window.mainloop()

# Starten der Threads für Fenster
settings_thread = Thread(target=run_settings_window)
fps_thread = Thread(target=run_fps_window)
video_thread = Thread(target=video_stream)

settings_thread.start()
fps_thread.start()
video_thread.start()

# Warten bis alle Threads abgeschlossen sind
settings_thread.join()
fps_thread.join()
video_thread.join()
