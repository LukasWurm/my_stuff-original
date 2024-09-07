import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import time
import matplotlib.pyplot as plt
from collections import deque
import threading
import json
import matplotlib.colors as mcolors
import mediapipe as mp
from PIL import ImageGrab

############################# Globale Variablen Anfang ##############################
color_options = {
    "Green": (0, 255, 0),
    "Red": (0, 0, 255),
    "Blue": (255, 0, 0),
    "Yellow": (0, 255, 255),
    "Cyan": (255, 255, 0),
    "White": (255, 255, 255),
    "Black": (0, 0, 0)
}

# Farbdarstellung Umwandlung
def rgb_to_hex(rgb):
    return mcolors.to_hex(rgb)

def hex_to_rgb(hex_color):
    return mcolors.hex2color(hex_color)

# Setze die Hintergrundfarbe
window_background_color = rgb_to_hex(color_options["Black"])  # Hintergrundfarbe für alle Fenster

# OpenCV Gesichtserkennungsmodell laden
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('c:/Users/User/Downloads/hand-gesture-recognition-mediapipe-main/hand-gesture-recognition-mediapipe-main/Ai Tracking Stuff/trainer.yml')


# Namen aus JSON-Datei laden
with open('c:/Users/User/Downloads/hand-gesture-recognition-mediapipe-main/hand-gesture-recognition-mediapipe-main/Ai Tracking Stuff/names.json', 'r') as file:
    name_data = json.load(file)

# Initialisieren von Mediapipe
mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)

# Feature-Flags und Einstellungen
hand_tracking_enabled = False
face_tracking_enabled = False
hand_confidence = 0.5
face_confidence = 0.5
fps = 0
avg_fps = 0
fps_data = []
avg_fps_data = []
color_name = "Green"
color = color_options[color_name]
flip_horizontal = True
flip_vertical = False
max_rendered_hands = 2
max_slider_value = 10
settings_window_size = (500, 450)
set_slider_length = 300
connection_dot_color = color_options["Blue"]
connection_color = color_options["Red"]
landmark_radius = 5
use_dynamic_face_tracking_color = False
use_separate_face_tracking_color = False
exit_event = False
edit_color_button = None
current_feed = "camera"
capture = None

############################## Globale Variablen Ende ##############################

# Initialize global variables
tracking_box_color = color_options[color_name]  # Default tracking box color
separate_face_tracking_color = color_options["Red"]  # Default face tracking color

# Function to toggle hand tracking
def toggle_hand_tracking():
    global hand_tracking_enabled
    hand_tracking_enabled = not hand_tracking_enabled

# Function to toggle face tracking
def toggle_face_tracking():
    global face_tracking_enabled
    face_tracking_enabled = not face_tracking_enabled

# Function to toggle dynamic box color
def toggle_dynamic_box_color():
    global use_dynamic_face_tracking_color
    use_dynamic_face_tracking_color = not use_dynamic_face_tracking_color

# Function to toggle separate face tracking color
def toggle_separate_face_color():
    global use_separate_face_tracking_color
    use_separate_face_tracking_color = not use_separate_face_tracking_color
    if use_separate_face_tracking_color:
        configure_separate_face_tracking_color_button.grid(row=3, column=1, padx=5, pady=5)
    else:
        configure_separate_face_tracking_color_button.grid_remove()

# Function to configure separate face tracking color
def configure_separate_face_tracking_color():
    separate_color_window = tk.Toplevel(root)
    separate_color_window.title("Configure Face Tracking Color")
    exit_button = tk.Button(separate_color_window, text="Exit", command=separate_color_window.destroy)
    exit_button.pack(pady=10)

# Function to update the tracking box color
def update_tracking_box_color():
    global tracking_box_color
    color = askcolor(title="Choose tracking box color")[0]
    if color:
        tracking_box_color = tuple(int(c) for c in color)

# Function to update the separate face tracking color
def update_separate_face_tracking_color():
    global separate_face_tracking_color
    color = askcolor(title="Choose separate face tracking color")[0]
    if color:
        separate_face_tracking_color = tuple(int(c) for c in color)

# Function to switch to desktop feed
def switch_to_desktop_feed():
    global current_feed
    current_feed = "desktop"

# Function to switch to camera feed
def switch_to_camera_feed():
    global current_feed
    current_feed = "camera"

# Function to calculate FPS
def calculate_fps(start_time, end_time):
    global fps, avg_fps
    elapsed_time = end_time - start_time
    fps = 1 / elapsed_time if elapsed_time > 0 else 0
    fps_data.append(fps)
    avg_fps = sum(fps_data) / len(fps_data) if fps_data else 0
    return fps

# Function to plot FPS
def plot_fps():
    plt.figure()
    plt.title("FPS Over Time")
    plt.xlabel("Frame")
    plt.ylabel("FPS")
    plt.plot(fps_data)
    plt.show()

# Function to process frames
def process_frames():
    global exit_event, capture, current_feed
    cap = cv2.VideoCapture(0)

    while not exit_event:
        start_time = time.time()
        ret, frame = cap.read()

        if not ret:
            break

        # Desktop feed capture
        if current_feed == "desktop":
            screenshot = np.array(ImageGrab.grab())
            frame = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # Hand tracking
        if hand_tracking_enabled:
            # Simulate hand tracking by drawing a rectangle (replace with actual hand tracking logic)
            cv2.rectangle(frame, (50, 50), (200, 200), tracking_box_color, 2)

        # Face tracking
        if face_tracking_enabled:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                if use_dynamic_face_tracking_color:
                    confidence = np.random.uniform(0.5, 1.0)  # Simulated confidence value
                    box_color = (0, int(255 * confidence), 0)
                elif use_separate_face_tracking_color:
                    box_color = separate_face_tracking_color
                else:
                    box_color = tracking_box_color

                cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)

        # Convert frame to ImageTk format for displaying in Tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        display_frame.imgtk = imgtk
        display_frame.configure(image=imgtk)

        end_time = time.time()
        calculate_fps(start_time, end_time)

        root.update_idletasks()
        root.update()

    cap.release()
    cv2.destroyAllWindows()

# Function to on-close the root window
def on_closing():
    global exit_event
    exit_event = True
    root.quit()

# Function to update GUI elements based on current settings
def update_settings_ui():
    if face_tracking_enabled:
        face_tracking_button.config(relief=tk.SUNKEN)
    else:
        face_tracking_button.config(relief=tk.RAISED)

    if hand_tracking_enabled:
        hand_tracking_button.config(relief=tk.SUNKEN)
    else:
        hand_tracking_button.config(relief=tk.RAISED)

    if use_dynamic_face_tracking_color:
        dynamic_color_button.config(relief=tk.SUNKEN)
    else:
        dynamic_color_button.config(relief=tk.RAISED)

    if use_separate_face_tracking_color:
        separate_face_color_button.config(relief=tk.SUNKEN)
        configure_separate_face_tracking_color_button.grid(row=3, column=1, padx=5, pady=5)
    else:
        separate_face_color_button.config(relief=tk.RAISED)
        configure_separate_face_tracking_color_button.grid_remove()

# Root window setup
root = tk.Tk()
root.title("Hand and Face Tracking")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Frame for video display
display_frame = tk.Label(root)
display_frame.pack()

# Settings window
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry(f"{settings_window_size[0]}x{settings_window_size[1]}")

    tab_control = ttk.Notebook(settings_window)

    # Tracking Tab
    tracking_tab = ttk.Frame(tab_control)
    tab_control.add(tracking_tab, text="Tracking")

    # Colors Tab
    colors_tab = ttk.Frame(tab_control)
    tab_control.add(colors_tab, text="Colors")

    tab_control.pack(expand=1, fill="both")

    # Tracking Options
    hand_tracking_button = ttk.Button(tracking_tab, text="Toggle Hand Tracking", command=toggle_hand_tracking)
    hand_tracking_button.grid(row=0, column=0, padx=5, pady=5)

    face_tracking_button = ttk.Button(tracking_tab, text="Toggle Face Tracking", command=toggle_face_tracking)
    face_tracking_button.grid(row=1, column=0, padx=5, pady=5)

    dynamic_color_button = ttk.Button(tracking_tab, text="Toggle Dynamic Face Tracking Color", command=toggle_dynamic_box_color)
    dynamic_color_button.grid(row=2, column=0, padx=5, pady=5)

    separate_face_color_button = ttk.Button(colors_tab, text="Toggle Separate Face Tracking Color", command=toggle_separate_face_color)
    separate_face_color_button.grid(row=0, column=0, padx=5, pady=5)

    configure_separate_face_tracking_color_button = ttk.Button(colors_tab, text="Configure Separate Face Tracking Color", command=configure_separate_face_tracking_color)
    configure_separate_face_tracking_color_button.grid(row=1, column=0, padx=5, pady=5)

    color_picker_button = ttk.Button(colors_tab, text="Select Tracking Box Color", command=update_tracking_box_color)
    color_picker_button.grid(row=2, column=0, padx=5, pady=5)

    update_settings_ui()

# Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add settings option to the menu bar
settings_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Open Settings", command=open_settings)

# Switch Feed Buttons
switch_frame = tk.Frame(root)
switch_frame.pack(pady=10)

camera_button = ttk.Button(switch_frame, text="Switch to Camera Feed", command=switch_to_camera_feed)
camera_button.grid(row=0, column=0, padx=5)

desktop_button = ttk.Button(switch_frame, text="Switch to Desktop Feed", command=switch_to_desktop_feed)
desktop_button.grid(row=0, column=1, padx=5)

# FPS Window
fps_window = tk.Toplevel(root)
fps_window.title("FPS")
fps_window.geometry("200x100")

fps_label = tk.Label(fps_window, text="FPS: Calculating...")
fps_label.pack(pady=10)

def update_fps_label():
    while not exit_event:
        if fps_data:
            fps_label.config(text=f"FPS: {fps_data[-1]:.2f}")
        time.sleep(1)

fps_thread = threading.Thread(target=update_fps_label, daemon=True)
fps_thread.start()

# WIP toggle button
wip_button = ttk.Button(fps_window, text="WIP", command=lambda: None)
wip_button.pack(pady=5)

# Start frame processing in a separate thread
process_thread = threading.Thread(target=process_frames, daemon=True)
process_thread.start()

# Start the Tkinter main loop
root.mainloop()
