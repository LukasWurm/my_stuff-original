import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import mediapipe as mp
import time
from threading import Thread

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Global variables
hand_tracking_mode = 2
min_confidence_face = 50.0
min_confidence_hand = 50.0
last_warning_time = 0
warning_displayed = False

def show_live_image(img, ax, fig):
    ax.clear()  # Clear previous image
    ax.axis('off')  # Hide axis
    if len(img.shape) == 2:  # If the image is grayscale
        ax.imshow(img, cmap='gray')
    else:  # If the image is in color
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    fig.canvas.draw()  # Update the figure
    plt.pause(0.001)  # Pause to allow matplotlib to update the figure

def process_hand_tracking(img):
    global last_warning_time, warning_displayed

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    current_time = time.time()
    
    if results.multi_hand_landmarks:
        num_hands = len(results.multi_hand_landmarks)
        
        if num_hands > hand_tracking_mode:
            if not warning_displayed:
                img = cv2.putText(img, "Too many hands!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                warning_displayed = True
                last_warning_time = current_time
        elif warning_displayed and (current_time - last_warning_time) < 2.5:
            img = cv2.putText(img, "Too many hands!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            warning_displayed = False  # Reset the flag if the condition is no longer met
        
        # Draw only up to the maximum allowed hands
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            if i >= hand_tracking_mode:
                break
            # Draw landmarks
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        warning_displayed = False  # Reset if no hands detected
    
    return img

def process_face_detection(img):
    global min_confidence_face, min_confidence_hand

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        id_, confidence = recognizer.predict(roi_gray)

        if confidence < (100 - min_confidence_face):  # Confidence threshold
            # Draw rectangle around detected face
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Display the name and confidence
            name = names[id_] if id_ < len(names) else "Unknown"
            cv2.putText(img, f"{name} ({confidence:.2f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return img

def update_hand_tracking_mode(value):
    global hand_tracking_mode
    hand_tracking_mode = int(round(float(value)))
    hand_tracking_label.config(text=f"Max Hand Render: {hand_tracking_mode}")

def update_min_confidence_face(value):
    global min_confidence_face
    min_confidence_face = float(value)
    min_confidence_face_label.config(text=f"Min Face Confidence: {min_confidence_face:.1f}")

def update_min_confidence_hand(value):
    global min_confidence_hand
    min_confidence_hand = float(value)
    min_confidence_hand_label.config(text=f"Min Hand Confidence: {min_confidence_hand:.1f}")

def create_settings_window():
    global hand_tracking_label, settings_window
    global min_confidence_face_slider, min_confidence_face_label
    global min_confidence_hand_slider, min_confidence_hand_label

    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x300")

    # Hand tracking slider
    hand_tracking_label = ttk.Label(settings_window, text=f"Max Hand Render: {hand_tracking_mode}")
    hand_tracking_label.pack(pady=10)
    hand_tracking_slider = ttk.Scale(settings_window, from_=1, to_=10, orient="horizontal", command=update_hand_tracking_mode)
    hand_tracking_slider.set(hand_tracking_mode)
    hand_tracking_slider.pack(pady=10)

    # Min confidence face slider
    min_confidence_face_label = ttk.Label(settings_window, text=f"Min Face Confidence: {min_confidence_face:.1f}")
    min_confidence_face_label.pack(pady=10)
    min_confidence_face_slider = ttk.Scale(settings_window, from_=0, to_=100, orient="horizontal", command=update_min_confidence_face)
    min_confidence_face_slider.set(min_confidence_face)
    min_confidence_face_slider.pack(pady=10)

    # Min confidence hand slider
    min_confidence_hand_label = ttk.Label(settings_window, text=f"Min Hand Confidence: {min_confidence_hand:.1f}")
    min_confidence_hand_label.pack(pady=10)
    min_confidence_hand_slider = ttk.Scale(settings_window, from_=0, to_=100, orient="horizontal", command=update_min_confidence_hand)
    min_confidence_hand_slider.set(min_confidence_hand)
    min_confidence_hand_slider.pack(pady=10)

def create_fps_window():
    global fps_label
    fps_window = tk.Toplevel(root)
    fps_window.title("FPS")
    fps_window.geometry("200x100")
    fps_label = ttk.Label(fps_window, text="FPS: 0")
    fps_label.pack(pady=20)

def on_escape(event):
    root.quit()
    root.destroy()
    if 'settings_window' in globals() and settings_window:
        settings_window.destroy()
    if 'fps_window' in globals() and fps_window:
        fps_window.destroy()

def run_main_loop():
    global prev_frame_time

    # Video Capture from the default camera (camera index 0)
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # Set width
    cam.set(4, 480)  # Set height

    # Minimum width and height for the window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    # Setup the matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.ion()  # Turn on interactive mode
    fig.show()

    prev_frame_time = time.time()

    while True:
        # Capture frame-by-frame
        ret, img = cam.read()
        if not ret:
            break

        # Process the image for hand tracking
        img = process_hand_tracking(img)

        # Process the image for face detection
        img = process_face_detection(img)

        # Calculate FPS
        new_frame_time = time.time()
        fps = int(1 / (new_frame_time - prev_frame_time))
        prev_frame_time = new_frame_time

        # Update the FPS label
        if 'fps_label' in globals() and fps_label:
            fps_label.config(text=f"FPS: {fps}")

        # Display the live image using matplotlib
        show_live_image(img, ax, fig)

        # Check for window closing
        if cv2.getWindowProperty('Live Feed', cv2.WND_PROP_VISIBLE) < 1:
            break

    # Release the camera and close all windows
    cam.release()
    cv2.destroyAllWindows()

# Initialize the Tkinter root window
root = tk.Tk()
root.title("Hand Gesture Recognition")
root.geometry("300x150")
root.bind("<Escape>", on_escape)

# Create the settings and FPS windows
create_settings_window()
create_fps_window()

# Run the main loop in a separate thread
main_thread = Thread(target=run_main_loop)
main_thread.start()

# Start the Tkinter event loop
root.mainloop()
