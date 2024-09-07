# Cheat Sheet für pynput - Tastatureingaben und Mauskontrolle

# Importiere die erforderlichen Module von pynput
from pynput import keyboard, mouse
import time

# Globale Variablen zum Steuern des Programmflusses
continue_program = False

# Callback-Funktion für Tasteneingaben
def on_press(key):
    """
    Callback-Funktion, die aufgerufen wird, wenn eine Taste gedrückt wird.
    :param key: Das gedrückte Tastenevent
    """
    global continue_program
    try:
        # Überprüfe, ob die gedrückte Taste die 'q'-Taste ist
        if key.char == 'q':
            continue_program = True
    except AttributeError:
        # Bei Sondertasten (z.B. Shift, Ctrl) wird AttributeError geworfen,
        # da diese Tasten keinen 'char'-Wert haben.
        pass

def wait_for_keypress():
    """
    Diese Funktion wartet, bis der Benutzer eine bestimmte Taste drückt,
    um den Programmfluss fortzusetzen.
    """
    global continue_program
    print("Drücke 'q', um fortzufahren...")  # Aufforderung an den Benutzer
    
    # Erstelle einen Tasteneingabe-Listener
    with keyboard.Listener(on_press=on_press) as listener:
        # Schleife warten, bis 'continue_program' auf True gesetzt wird
        while not continue_program:
            pass  # Leere Schleife, um auf Tastendruck zu warten
        
        # Stoppe den Listener, wenn die Bedingung erfüllt ist
        listener.stop()

# Beispielnutzung für Tasteneingaben
print("Beispiel 1: Beginne...")
wait_for_keypress()  # Warte auf Tastendruck
print("Weiter mit dem nächsten Abschnitt.")

# Maussteuerung:

# Callback-Funktion für Mausbewegungen
def on_move(x, y):
    """
    Callback-Funktion, die aufgerufen wird, wenn die Maus bewegt wird.
    :param x: X-Koordinate der Maus
    :param y: Y-Koordinate der Maus
    """
    print(f"Maus bewegt zu ({x}, {y})")

# Callback-Funktion für Mausklicks
def on_click(x, y, button, pressed):
    """
    Callback-Funktion, die aufgerufen wird, wenn ein Mausklick erfolgt.
    :param x: X-Koordinate des Klicks
    :param y: Y-Koordinate des Klicks
    :param button: Der Mausklick-Button (left, right, middle)
    :param pressed: Wahr, wenn der Button gedrückt wird, sonst False
    """
    if pressed:
        print(f"Button {button} gedrückt bei ({x}, {y})")
    else:
        print(f"Button {button} losgelassen bei ({x}, {y})")

# Beispielnutzung für Maussteuerung
print("Maussteuerung aktiv. Bewege die Maus oder klicke, um Daten zu sehen.")

# Erstelle einen Maus-Listener
with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
    # Der Listener läuft hier endlos, bis das Programm beendet wird.
    # Wenn du den Listener nur für eine bestimmte Zeit laufen lassen möchtest,
    # kannst du dies durch eine Zeitverzögerung erreichen.
    
    # Hinweis: Um den Listener nach einer bestimmten Zeit zu beenden, 
    # kannst du die folgende Zeile verwenden:
    # time.sleep(10)  # Warten für 10 Sekunden
    
    # Stoppe den Listener, nachdem die Wartezeit abgelaufen ist
    # listener.stop()
    
    listener.join()  # Warte, bis der Listener beendet wird

# Hinweis: Der Maus-Listener wird nicht automatisch beendet.
# Du musst das Programm manuell beenden oder eine Methode implementieren,
# um den Listener zu stoppen, wenn ein bestimmtes Ereignis eintritt.
