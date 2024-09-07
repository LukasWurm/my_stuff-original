import tkinter as tk  # Importiert das Tkinter-Modul für GUI-Erstellung
from tkinter import messagebox  # Importiert das Modul für Dialogboxen
import threading  # Importiert das Threading-Modul für paralleles Ausführen

# -------------------------
# Tkinter: Grundlegendes Setup und Widgets
# -------------------------

# Hauptfenster erstellen
root = tk.Tk()  # Erstellt ein Hauptfenster
root.title("Mein Tkinter Programm")  # Setzt den Titel des Fensters
root.geometry("400x300")  # Setzt die Größe des Fensters (Breite x Höhe)

# Label Widget
# Ein Label zeigt Text an.
label = tk.Label(root, text="Willkommen zu meinem Programm!", font=("Arial", 14))
label.pack(pady=20)  # Packt das Label in das Fenster mit etwas Abstand nach oben (pady)

# Button Widget
# Ein Button führt eine Funktion aus, wenn er geklickt wird.
def button_click():
    label.config(text="Button wurde geklickt!")  # Ändert den Text des Labels
button = tk.Button(root, text="Klick mich!", command=button_click)
button.pack(pady=10)

# Entry Widget
# Ein Entry ist ein Textfeld, in das der Benutzer Text eingeben kann.
entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=10)

# Messagebox
# Eine Messagebox zeigt eine Dialogbox an.
def show_message():
    messagebox.showinfo("Information", "Das ist eine Messagebox!")  # Zeigt eine Informationsbox an
msg_button = tk.Button(root, text="Zeige Nachricht", command=show_message)
msg_button.pack(pady=10)

# -------------------------
# Tkinter: Canvas und Zeichnungen
# -------------------------

# Canvas Widget
# Ein Canvas erlaubt das Zeichnen von Formen, Linien und Text.
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack(pady=20)

# Zeichnet ein Rechteck auf das Canvas
rect = canvas.create_rectangle(50, 50, 250, 150, fill="blue")

# -------------------------
# Threading: Parallele Ausführung in Tkinter
# -------------------------

# Threading Einführung
# Threading erlaubt das parallele Ausführen von Funktionen, was wichtig ist, um die GUI reaktionsfähig zu halten.

def long_running_task():
    import time
    for i in range(5):
        print(f"Langlaufender Task läuft... {i + 1}")
        time.sleep(1)
    label.config(text="Task abgeschlossen!")  # Aktualisiert das Label nach Abschluss des Tasks

# Thread starten
def start_thread():
    thread = threading.Thread(target=long_running_task)  # Erstellt einen Thread, der die Funktion ausführt
    thread.start()  # Startet den Thread

thread_button = tk.Button(root, text="Starte langen Task", command=start_thread)
thread_button.pack(pady=10)

# -------------------------
# Tkinter: Haupt-Loop starten
# -------------------------

# Dies startet die Haupt-Loop des Tkinter-Fensters und wartet auf Benutzeraktionen.
root.mainloop()

# ----------------------------------------
# Erklärungen zu den Konzepten
# ----------------------------------------

# Tkinter Widgets:
# - `Label`: Dient zur Anzeige von Text im Fenster.
# - `Button`: Ein interaktiver Button, der eine Funktion auslöst, wenn er geklickt wird.
# - `Entry`: Ein Eingabefeld, in das der Benutzer Text eingeben kann.
# - `Messagebox`: Zeigt Dialogboxen wie Information, Warnung, etc. an.
# - `Canvas`: Eine Fläche, auf der Formen, Linien oder Text gezeichnet werden können.

# Tkinter Layout-Management:
# - `pack()`: Einfaches Layout, bei dem Widgets der Reihe nach angeordnet werden.
# - `grid()`: Rasterlayout, bei dem Widgets in einem Gitternetz angeordnet werden.
# - `place()`: Absolute Positionierung, bei der Widgets an exakten Koordinaten platziert werden.

# Threading:
# - `threading.Thread`: Erstellt einen neuen Thread, der eine Funktion parallel zur Hauptausführung ausführt.
# - `thread.start()`: Startet den Thread und führt die zugehörige Funktion aus.
# - Wichtig: Die Haupt-Loop von Tkinter (`root.mainloop()`) muss im Hauptthread laufen. Threads sind nützlich, um langlaufende Aufgaben auszuführen, ohne die GUI zu blockieren.

# Warum Threading in Tkinter?
# Tkinter ist "Single-threaded", das heißt, es verarbeitet alle GUI-Aktionen im Hauptthread. Wenn du eine langlaufende Aufgabe ausführst (z.B. eine Berechnung), ohne sie in einem separaten Thread zu starten, friert die GUI ein und wird nicht mehr aktualisiert. Threading löst dieses Problem, indem es die Aufgabe in den Hintergrund verlagert, während Tkinter weiterhin auf Benutzereingaben reagiert.
