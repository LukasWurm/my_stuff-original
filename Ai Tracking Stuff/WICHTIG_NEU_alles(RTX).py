# import yaml
import cv2
import json
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
import mediapipe as mp 
import numpy as np # type: ignore
import matplotlib.pyplot as plt 
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 



# Mediapipe initialisieren
mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)


# Globale Variablen


# Createing Colors
color_options = {
    "Green": (0, 255, 0),
    "Red": (0, 0, 255),
    "Blue": (255, 0, 0),
    "Yellow": (0, 255, 255),
    "Cyan": (255, 255, 0),
    "White" : (255, 255, 255),
    "Black" : (0, 0, 0)
}

# OpenCV Gesichtserkennungsmodell laden
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

# Namen aus JSON-Datei laden
with open('names.json', 'r') as file:
    name_data = json.load(file)


# Enable Tracking
hand_tracking_enabled = False
face_tracking_enabled = False

# Min Confidence

hand_confidence = 0.5
face_confidence = 0.5

# FPS

fps = 0
avg_fps = 0
fps_data = []
avg_fps_data = []

# Setup for color and exiting

exit_event = False
color_name = "Green"
color = color_options[color_name]

# Default Settings and Settings Window Settings

flip_horizontal = True
flip_vertical = False
max_rendered_hands = 2
max_slider_value = 10
settings_window_size = (500, 450)
set_slider_length = 300

# Default Hand-Tracking Colors

connection_dot_color = color_options["Red"]
connection_color = color_options["Blue"]
landmark_radius = 5

# Globale Variablen Ende

# GUI-Elemente
hand_confidence_value_label = None
face_confidence_value_label = None
max_rendered_hands_value_label = None


# Hands-Instanz global definieren, um bei Änderung der Anzahl der Hände neu zu initialisieren

hands = mp_hands.Hands(max_num_hands=max_rendered_hands, min_detection_confidence=0.7)

def update_hand_recognition_settings():
    global hands
    hands = mp_hands.Hands(max_num_hands=max_rendered_hands, min_detection_confidence=hand_confidence)


# Hand-Tracking-Funktion

def track_hands(frame):
    global hand_confidence, connection_color, landmark_radius, connection_dot_color
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            h, w, _ = frame.shape

            # Zeichne Linien zwischen den Landmarken
            connections = mp_hands.HAND_CONNECTIONS
            for connection in connections:
                start_idx, end_idx = connection
                start_landmark = landmarks[start_idx]
                end_landmark = landmarks[end_idx]
                start_x, start_y = int(start_landmark.x * w), int(start_landmark.y * h)
                end_x, end_y = int(end_landmark.x * w), int(end_landmark.y * h)
                cv2.line(frame, (start_x, start_y), (end_x, end_y), connection_color, 2)

            # Zeichne die Landmarken als Kreise
            for landmark in landmarks:
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (x, y), landmark_radius, connection_dot_color, -1)



# Gesichtserkennung-Funktion

def track_faces(frame):
    global face_confidence
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.detections:
        for detection in results.detections:
            detection_conf = detection.score[0]
            if detection_conf >= face_confidence:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                
                # Überprüfen, ob die Bounding Box innerhalb des Bildrahmens liegt
                if x < 0 or y < 0 or x + w > iw or y + h > ih or w <= 0 or h <= 0:
                    continue

                # Gesichtsausschnitt erstellen und Größe überprüfen
                face = gray_frame[y:y+h, x:x+w]
                if face.size == 0:
                    continue

                # Vorhersage mit dem Gesichtserkennungsmodell
                try:
                    label, confidence = recognizer.predict(face)

                    # Name der erkannten Person basierend auf dem Label
                    recognized_name = name_data.get(str(label), "Unknown")

                    # Zeichne das Rechteck um das Gesicht und zeige den Namen und die Genauigkeit
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, f'Name: {recognized_name}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(frame, f'Confidence: {confidence:.2f}%', (x + w - 120, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                except cv2.error as e:
                    print(f"Error predicting face: {e}")

def video_stream():
    global fps, avg_fps, hand_tracking_enabled, face_tracking_enabled, flip_horizontal, flip_vertical, max_rendered_hands
    cap = cv2.VideoCapture(0)
    prev_time = 0
    total_frames = 0
    start_time = time.time()

    while not exit_event:
        ret, frame = cap.read()
        if not ret:
            continue

        if flip_horizontal:
            frame = cv2.flip(frame, 1)
        if flip_vertical:
            frame = cv2.flip(frame, 0)

        if hand_tracking_enabled:
            track_hands(frame)

        if face_tracking_enabled:
            track_faces(frame)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(image=frame_pil)

        camera_label.config(image=frame_tk)
        camera_label.image = frame_tk

        # FPS Berechnung
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        total_frames += 1
        avg_fps = total_frames / (current_time - start_time)

        # FPS-Daten aktualisieren
        fps_data.append(fps)
        avg_fps_data.append(avg_fps)
        if len(fps_data) > 100:
            fps_data.pop(0)
            avg_fps_data.pop(0)

    cap.release()

def set_hand_confidence(value):
    global hand_confidence
    hand_confidence = float(value)
    if hand_confidence_value_label:
        hand_confidence_value_label.config(text=f"{hand_confidence:.2f}")
    update_hand_recognition_settings()

def set_face_confidence(value):
    global face_confidence
    face_confidence = float(value)
    if face_confidence_value_label:
        face_confidence_value_label.config(text=f"{face_confidence:.2f}")

def set_max_rendered_hands(value):
    global max_rendered_hands
    try:
        max_rendered_hands = int(float(value))
        if max_rendered_hands_value_label:
            max_rendered_hands_value_label.config(text=f"{max_rendered_hands}")
        update_hand_recognition_settings()
    except ValueError:
        pass  # Ungültiger Wert

def change_color(selected_color):
    global color, color_name
    color_name = selected_color
    color = color_options[color_name]

def toggle_feature(feature):
    global hand_tracking_enabled, face_tracking_enabled
    if feature == 'hand':
        hand_tracking_enabled = not hand_tracking_enabled
    elif feature == 'face':
        face_tracking_enabled = not face_tracking_enabled

def toggle_flip(direction):
    global flip_horizontal, flip_vertical
    if direction == 'horizontal':
        flip_horizontal = not flip_horizontal
    elif direction == 'vertical':
        flip_vertical = not flip_vertical

def run_settings_window():
    global hand_tracking_enabled, face_tracking_enabled, flip_horizontal, flip_vertical, settings_window_size, set_slider_length

    # Standardmäßig deaktivieren wir das Hand- und Face-Tracking
    # hand_tracking_enabled = False
    # face_tracking_enabled = False
    # flip_horizontal = True
    # flip_vertical = False

    settings_window = tk.Toplevel(main_window)
    settings_window.title("Settings")
    settings_window.geometry(f"{settings_window_size[0]}x{settings_window_size[1]}")
    settings_window.configure(bg="gray")

    slider_length = set_slider_length  # Länge der Slider anpassen

    hand_confidence_label = tk.Label(settings_window, text="Hand Confidence:", bg="gray", fg="white")
    hand_confidence_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
    hand_confidence_slider = ttk.Scale(settings_window, from_=0.1, to=1.0, orient=tk.HORIZONTAL, command=set_hand_confidence, length=slider_length)
    hand_confidence_slider.set(hand_confidence)
    hand_confidence_slider.grid(row=0, column=1, sticky=tk.EW, padx=10)
    global hand_confidence_value_label
    hand_confidence_value_label = tk.Label(settings_window, text=f"{hand_confidence:.2f}", bg="gray", fg="white")
    hand_confidence_value_label.grid(row=0, column=2, padx=10)

    # Face Confidence
    face_confidence_label = tk.Label(settings_window, text="Face Confidence:", bg="gray", fg="white")
    face_confidence_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    face_confidence_slider = ttk.Scale(settings_window, from_=0.1, to=1.0, orient=tk.HORIZONTAL, command=set_face_confidence, length=slider_length)
    face_confidence_slider.set(face_confidence)
    face_confidence_slider.grid(row=1, column=1, sticky=tk.EW, padx=10)
    global face_confidence_value_label
    face_confidence_value_label = tk.Label(settings_window, text=f"{face_confidence:.2f}", bg="gray", fg="white")
    face_confidence_value_label.grid(row=1, column=2, padx=10)

    # Max Rendered Hands
    max_rendered_hands_label = tk.Label(settings_window, text="Max Rendered Hands:", bg="gray", fg="white")
    max_rendered_hands_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    max_rendered_hands_slider = ttk.Scale(settings_window, from_=1, to=max_slider_value, orient=tk.HORIZONTAL, command=set_max_rendered_hands, length=slider_length)
    max_rendered_hands_slider.set(max_rendered_hands)
    max_rendered_hands_slider.grid(row=2, column=1, sticky=tk.EW, padx=10)
    global max_rendered_hands_value_label
    max_rendered_hands_value_label = tk.Label(settings_window, text=f"{max_rendered_hands}", bg="gray", fg="white")
    max_rendered_hands_value_label.grid(row=2, column=2, padx=10)

    # Farbeinstellungen
    color_label = tk.Label(settings_window, text="Select Color:", bg="gray", fg="white")
    color_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    color_menu = ttk.Combobox(settings_window, values=list(color_options.keys()))
    color_menu.set(color_name)
    color_menu.grid(row=3, column=1, sticky=tk.EW, padx=10)
    color_menu.bind("<<ComboboxSelected>>", lambda event: change_color(color_menu.get()))

    # Toggle Buttons
    toggle_hand = tk.Button(settings_window, text=f"Toggle Hand Tracking ({hand_tracking_enabled})", bg="gray", fg="white", command=lambda: toggle_feature('hand', toggle_hand))
    toggle_hand.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

    toggle_face = tk.Button(settings_window, text=f"Toggle Face Tracking ({face_tracking_enabled})", bg="gray", fg="white", command=lambda: toggle_feature('face', toggle_face))
    toggle_face.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

    toggle_horizontal = tk.Button(settings_window, text=f"Flip Horizontal ({flip_horizontal})", bg="gray", fg="white", command=lambda: toggle_flip('horizontal', toggle_horizontal))
    toggle_horizontal.grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

    toggle_vertical = tk.Button(settings_window, text=f"Flip Vertical ({flip_vertical})", bg="gray", fg="white", command=lambda: toggle_flip('vertical', toggle_vertical))
    toggle_vertical.grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

    toggle_dynamic_color = tk.Button(settings_window, text=f"Use Dynamic Face Tracking Color ({use_dynamic_face_tracking_color})", bg="gray", fg="white", command=lambda: toggle_dynamic_color_fn(toggle_dynamic_color))
    toggle_dynamic_color.grid(row=8, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)


def toggle_feature(feature, button):
    global hand_tracking_enabled, face_tracking_enabled
    if feature == 'hand':
        hand_tracking_enabled = not hand_tracking_enabled
        button.config(text=f"Toggle Hand Tracking ({hand_tracking_enabled})")
    elif feature == 'face':
        face_tracking_enabled = not face_tracking_enabled
        button.config(text=f"Toggle Face Tracking ({face_tracking_enabled})")
        
        
def toggle_flip(direction, button):
    global flip_horizontal, flip_vertical
    if direction == 'horizontal':
        flip_horizontal = not flip_horizontal
        button.config(text=f"Flip Horizontal ({flip_horizontal})")
    elif direction == 'vertical':
        flip_vertical = not flip_vertical
        button.config(text=f"Flip Vertical ({flip_vertical})")
        
def toggle_dynamic_color_fn(button):
    global use_dynamic_face_tracking_color
    use_dynamic_face_tracking_color = not use_dynamic_face_tracking_color
    button.config(text=f"Use Dynamic Face Tracking Color ({use_dynamic_face_tracking_color})")

def set_max_rendered_hands(value):
    global max_rendered_hands
    max_rendered_hands = int(float(value))  # Slider-Wert in eine Ganzzahl umwandeln
    max_rendered_hands_value_label.config(text=f"{max_rendered_hands}")

def run_fps_window():
    fps_window = tk.Toplevel(main_window)
    fps_window.title("FPS Data")
    fps_window.geometry("400x400")
    fps_window.configure(bg="gray")

    figure, ax = plt.subplots(facecolor='gray')
    ax.set_title('FPS Data')
    ax.set_xlabel('Time')
    ax.set_ylabel('FPS')
    ax.grid(True)

    line1, = ax.plot(fps_data, label="FPS", color="blue")
    line2, = ax.plot(avg_fps_data, label="Average FPS", color="red")

    ax.legend(loc='upper right')

    def update_plot():
        line1.set_ydata(fps_data)
        line2.set_ydata(avg_fps_data)
        ax.set_xlim(0, len(fps_data))
        ax.set_ylim(min(fps_data + avg_fps_data) - 5, max(fps_data + avg_fps_data) + 5)
        figure.canvas.draw()
        fps_window.after(100, update_plot)

    canvas = FigureCanvasTkAgg(figure, fps_window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    update_plot()

# Hauptprogramm
main_window = tk.Tk()
main_window.title("Hand & Face Recognition")
main_window.geometry("800x600")
main_window.configure(bg="gray")

camera_label = tk.Label(main_window)
camera_label.pack(padx=10, pady=10)

button_frame = tk.Frame(main_window, bg="gray")
button_frame.pack(padx=10, pady=10)

settings_button = tk.Button(button_frame, text="Settings", command=run_settings_window)
settings_button.pack(side=tk.LEFT, padx=10)

fps_button = tk.Button(button_frame, text="FPS Data", command=run_fps_window)
fps_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame, text="Exit", command=main_window.quit)
exit_button.pack(side=tk.LEFT, padx=10)

# Starte den Video-Thread
video_thread = Thread(target=video_stream, daemon=True)
video_thread.start()

# Starte die Haupt-Event-Schleife
main_window.mainloop()

# Beende das Programm
exit_event = True
video_thread.join()