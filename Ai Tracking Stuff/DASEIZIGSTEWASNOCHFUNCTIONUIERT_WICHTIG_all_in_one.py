import cv2
import mediapipe as mp
import tensorflow as tf
import numpy as np
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
from PIL import Image, ImageTk  # Für Bildkonvertierung
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# GPU Check
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Initialisieren der Mediapipe-Komponenten für Hand- und Gesichtserkennung
mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)

# Globale Variablen
hand_tracking_mode = 2
hand_confidence = 0.50
face_confidence = 0.70
fps = 0
avg_fps = 0
fps_count = 0
fps_sum = 0
exit_event = False
show_avg_fps = False
color = (0, 255, 0)  # Standardfarbe für die Bounding Box (grün)
camera_vertical_flip = False
camera_horizontal_flip = False
hand_tracking_enabled = False
face_tracking_enabled = False

# Globale Diagrammvariablen
fps_data = []
avg_fps_data = []

# FPS Zähler
last_time = time.time()

# Funktionen zur Hand- und Gesichtserkennung
def process_frame(frame):
    global last_time, fps, avg_fps, fps_count, fps_sum
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Hand-Erkennung
    if hand_tracking_enabled:
        results_hands = hands.process(image_rgb)
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks[:hand_tracking_mode]:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Gesichtserkennung
    if face_tracking_enabled:
        results_face = face_detection.process(image_rgb)
        if results_face.detections:
            for detection in results_face.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, f"{detection.score[0]:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
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

        if camera_vertical_flip:
            frame = cv2.flip(frame, 0)
        if camera_horizontal_flip:
            frame = cv2.flip(frame, 1)

        frame = process_frame(frame)
        
        # Convert frame to RGB format for Tkinter display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(image=frame_pil)
        
        if main_window:
            camera_label.config(image=frame_tk)
            camera_label.image = frame_tk
        
        time.sleep(0.01)  # Reduce CPU usage

    cap.release()

def run_settings_window():
    global hand_tracking_mode, hand_confidence, face_confidence
    global hand_tracking_slider, hand_confidence_slider, face_confidence_slider
    global hand_tracking_label, avg_fps_var

    settings_window = tk.Toplevel(main_window)
    settings_window.title("Settings")
    settings_window.geometry("300x400")  # Ursprüngliche Größe

    settings_window.grid_columnconfigure(0, weight=1)
    settings_window.grid_columnconfigure(1, weight=1)
    
    settings_window.grid_rowconfigure(0, weight=1)
    settings_window.grid_rowconfigure(1, weight=1)
    settings_window.grid_rowconfigure(2, weight=1)
    settings_window.grid_rowconfigure(3, weight=1)
    settings_window.grid_rowconfigure(4, weight=1)
    settings_window.grid_rowconfigure(5, weight=1)
    settings_window.grid_rowconfigure(6, weight=1)
    
    # Enable Hand und Face Tracking
    enable_hand_tracking = tk.BooleanVar(value=hand_tracking_enabled)
    enable_face_tracking = tk.BooleanVar(value=face_tracking_enabled)
    
    tk.Checkbutton(settings_window, text="Enable Hand Tracking", variable=enable_hand_tracking, command=toggle_hand_tracking).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    tk.Checkbutton(settings_window, text="Enable Face Tracking", variable=enable_face_tracking, command=toggle_face_tracking).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    # Hand Tracking
    hand_tracking_label = tk.Label(settings_window, text=f"Max Hand Render: {hand_tracking_mode}")
    hand_tracking_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    
    hand_tracking_slider = tk.Scale(settings_window, from_=1, to=10, orient=tk.HORIZONTAL, command=update_hand_tracking_mode)
    hand_tracking_slider.set(hand_tracking_mode)
    hand_tracking_slider.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    reset_hand_tracking_mode_button = tk.Button(settings_window, text="Reset Hand Tracking Mode", command=reset_hand_tracking_mode)
    reset_hand_tracking_mode_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
    
    # Confidence
    tk.Label(settings_window, text="Hand Confidence:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    hand_confidence_slider = tk.Scale(settings_window, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, command=lambda value: update_confidence(value, 'hand'))
    hand_confidence_slider.set(hand_confidence)
    hand_confidence_slider.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    reset_hand_confidence_button = tk.Button(settings_window, text="Reset Hand Confidence", command=reset_hand_confidence)
    reset_hand_confidence_button.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

    tk.Label(settings_window, text="Face Confidence:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
    face_confidence_slider = tk.Scale(settings_window, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, command=lambda value: update_confidence(value, 'face'))
    face_confidence_slider.set(face_confidence)
    face_confidence_slider.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

    reset_face_confidence_button = tk.Button(settings_window, text="Reset Face Confidence", command=reset_face_confidence)
    reset_face_confidence_button.grid(row=7, column=1, padx=10, pady=10, sticky="ew")
    
    # Weitere Optionen
    vertical_flip_button = tk.Button(settings_window, text="Vertical Flip Camera", command=toggle_camera_vertical_flip)
    vertical_flip_button.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

    horizontal_flip_button = tk.Button(settings_window, text="Horizontal Flip Camera", command=toggle_camera_horizontal_flip)
    horizontal_flip_button.grid(row=9, column=0, padx=10, pady=10, sticky="ew")
    
    color_button = tk.Button(settings_window, text="Change Box Color", command=change_box_color)
    color_button.grid(row=10, column=0, padx=10, pady=10, sticky="ew")
    
    avg_fps_var = tk.BooleanVar(value=show_avg_fps)
    avg_fps_checkbox = tk.Checkbutton(settings_window, text="Show Avg FPS", variable=avg_fps_var, command=toggle_avg_fps)
    avg_fps_checkbox.grid(row=11, column=0, padx=10, pady=10, sticky="w")

    def on_closing():
        settings_window.destroy()

    settings_window.protocol("WM_DELETE_WINDOW", on_closing)

def run_fps_window():
    global fps_label, avg_fps_label, exit_event, fps_chart_window

    fps_window = tk.Toplevel(main_window)
    fps_window.title("FPS Display")
    fps_window.geometry("400x200")  # Initialgröße

    fps_window.grid_columnconfigure(0, weight=1)
    fps_window.grid_rowconfigure(0, weight=1)
    fps_window.grid_rowconfigure(1, weight=1)
    fps_window.grid_rowconfigure(2, weight=1)

    fps_label = tk.Label(fps_window, text=f"FPS: {fps}")
    fps_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    avg_fps_label = tk.Label(fps_window, text="")
    avg_fps_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    fps_button = tk.Button(fps_window, text="Show FPS Chart", command=show_fps_chart)
    fps_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def update_fps():
        global fps, avg_fps
        if fps_label:
            fps_label.config(text=f"FPS: {fps}")
            if show_avg_fps:
                avg_fps_label.config(text=f"Avg FPS: {avg_fps:.2f}")
            else:
                avg_fps_label.config(text="")

    def adjust_label_font(label, window):
        width = window.winfo_width()
        font_size = int(width / 20)  # Schriftgröße proportional zur Fensterbreite
        label.config(font=("Arial", font_size))

    def update_fps_display_loop():
        global exit_event

        while not exit_event:
            update_fps()
            adjust_label_font(fps_label, fps_window)
            adjust_label_font(avg_fps_label, fps_window)
            time.sleep(1)  # Aktualisierungsintervall für die FPS-Anzeige

        if fps_window:
            fps_window.destroy()

    # Starten eines Threads für das Update der FPS-Anzeige
    Thread(target=update_fps_display_loop, daemon=True).start()

    def on_closing():
        global exit_event
        exit_event = True
        fps_window.destroy()

    fps_window.protocol("WM_DELETE_WINDOW", on_closing)

def show_fps_chart():
    global fps_chart_window, exit_event

    fps_chart_window = tk.Toplevel(main_window)
    fps_chart_window.title("FPS Chart")
    fps_chart_window.geometry("600x400")  # Initialgröße für das Diagramm

    fig, ax = plt.subplots()
    ax.set_ylim(0, 130)
    ax.set_xlim(0, 10)  # Zeitspanne von 10 Sekunden
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('FPS')
    ax.set_title('FPS Chart')

    global fps_data, avg_fps_data
    fps_data = []
    avg_fps_data = []

    line_fps, = ax.plot([], [], 'b-', label='Current FPS')
    line_avg_fps, = ax.plot([], [], 'r-', label='Avg FPS (Last 10s)')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=fps_chart_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_chart():
        global fps_data, avg_fps_data
        while not exit_event:
            fps_data.append(fps)
            if len(fps_data) > 50:
                fps_data.pop(0)
            x_data = list(range(len(fps_data)))

            avg_fps_data.append(avg_fps)
            if len(avg_fps_data) > 50:
                avg_fps_data.pop(0)
            
            line_fps.set_data(x_data, fps_data)
            line_avg_fps.set_data(x_data, avg_fps_data)
            
            ax.relim()
            ax.autoscale_view()
            canvas.draw_idle()  # Update für Matplotlib-Canvas
            time.sleep(0.1)  # Intervall für das Update des Diagramms

    # Starten eines Threads für das Update des Diagramms
    Thread(target=update_chart, daemon=True).start()

    def on_closing():
        global exit_event
        exit_event = True
        fps_chart_window.destroy()

    fps_chart_window.protocol("WM_DELETE_WINDOW", on_closing)

def reset_hand_tracking_mode():
    hand_tracking_slider.set(2)
    update_hand_tracking_mode(2)

def reset_hand_confidence():
    hand_confidence_slider.set(0.50)
    update_confidence(0.50, 'hand')

def reset_face_confidence():
    face_confidence_slider.set(0.70)
    update_confidence(0.70, 'face')

def update_hand_tracking_mode(value):
    global hand_tracking_mode
    hand_tracking_mode = int(float(value))
    if hand_tracking_label:
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

def toggle_hand_tracking():
    global hand_tracking_enabled
    hand_tracking_enabled = not hand_tracking_enabled

def toggle_face_tracking():
    global face_tracking_enabled
    face_tracking_enabled = not face_tracking_enabled

def toggle_camera_vertical_flip():
    global camera_vertical_flip
    camera_vertical_flip = not camera_vertical_flip

def toggle_camera_horizontal_flip():
    global camera_horizontal_flip
    camera_horizontal_flip = not camera_horizontal_flip

def change_box_color():
    global color
    # Beispielhafte Farbänderung
    color = (255, 0, 0) if color == (0, 255, 0) else (0, 255, 0)

def create_main_window():
    global main_window, camera_label

    main_window = tk.Tk()
    main_window.title("Main Window")
    main_window.geometry("1200x600")  # Größeres Fenster für Sidebar und Kamera Feed

    # Camera Feed Frame
    camera_frame = tk.Frame(main_window, width=800, height=600, bg='black')
    camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Kamera-Label für das Kamera-Feed
    camera_label = tk.Label(camera_frame)
    camera_label.pack(fill=tk.BOTH, expand=True)
    
    # Sidebar Frame
    sidebar = tk.Frame(main_window, width=400, bg='gray')
    sidebar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Buttons in der Sidebar
    open_settings_button = tk.Button(sidebar, text="Open Settings", command=run_settings_window)
    open_settings_button.pack(pady=10)
    
    open_fps_button = tk.Button(sidebar, text="Open FPS Display", command=run_fps_window)
    open_fps_button.pack(pady=10)
    
    open_empty_button = tk.Button(sidebar, text="Open Empty Window", command=lambda: tk.Toplevel(main_window))
    open_empty_button.pack(pady=10)

    # Start Video Stream
    video_thread = Thread(target=video_stream, daemon=True)
    video_thread.start()

    main_window.mainloop()

create_main_window()
