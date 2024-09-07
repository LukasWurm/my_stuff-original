# Cheat Sheet für die Programmierung eines Arduinos mit Python und Firmata

import pyfirmata
import time



                                     # Verbinde mit dem Arduino über den richtigen Port
                                     # Ersetze 'COM3' durch den tatsächlichen Port deines Arduinos
board = pyfirmata.Arduino('COM4')


                                     # Starte einen Iterator für die serielle Kommunikation
                                     # Der Iterator sorgt dafür, dass alle Daten vom Arduino regelmäßig verarbeitet werden
                                     # Dies wird verwendet, wenn daten von dem Arduino empfangen werden sollen
it = pyfirmata.util.Iterator(board)
it.start()

start = input("Start?")

sensor_pin = board.get_pin('a:0:i')  # Analoger Pin 0 als Eingang

def read_analog_pin(pin):
    """
    Lese den Wert eines analogen Pins.
    :param pin: Der Pin, der gelesen werden soll (Pyfirmata Pin-Objekt)
    :return: Der Wert des Pins (0.0 bis 1.0)
    """
    return pin.read()

def on_click(pressed):
    if not pressed:
        return  # Use return instead of break to exit the function

# 3. Analoger Sensorwert lesen:
print("Analoger Sensorwert lesen Beispiel")
start = input("Start?")
while True:
    

    
    # start = input("Read?")
    sensor_value = sensor_pin.read()
    if sensor_value is not None:
        print(f'Sensorwert: {sensor_value:.2f}')
    else:
        print("Sensorwert ist None")
        
    time.sleep(0.1)





# Abschluss:
print("Beispielcode abgeschlossen")
