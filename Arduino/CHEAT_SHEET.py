# Cheat Sheet für die Programmierung eines Arduinos mit Python und Firmata

import pyfirmata
import time

start = input("Start?")

                                     # Verbinde mit dem Arduino über den richtigen Port
                                     # Ersetze 'COM3' durch den tatsächlichen Port deines Arduinos
board = pyfirmata.Arduino('COM4')


                                     # Starte einen Iterator für die serielle Kommunikation
                                     # Der Iterator sorgt dafür, dass alle Daten vom Arduino regelmäßig verarbeitet werden
                                     # Dies wird verwendet, wenn daten von dem Arduino empfangen werden sollen
it = pyfirmata.util.Iterator(board)
it.start()



                                     # Pin-Konfigurationen:
                                     # Definiere den Pin für einen digitalen Eingang (z.B. Taster)
button_pin = board.get_pin('d:2:i')  # Digitaler Pin 2 als Eingang

                                     # Definiere den Pin für einen digitalen Ausgang (z.B. LED)
led_pin = board.get_pin('d:13:o')    # Digitaler Pin 13 als Ausgang

                                     # Definiere den Pin für einen analogen Eingang (z.B. Sensor)
sensor_pin = board.get_pin('a:0:i')  # Analoger Pin 0 als Eingang

# Funktionen:
def read_digital_pin(pin):
    """
    Lese den Status eines digitalen Pins.
    :param pin: Der Pin, der gelesen werden soll (Pyfirmata Pin-Objekt)
    :return: Der Status des Pins (True/False)
    """
    return pin.read()

def write_digital_pin(pin, value):
    """
    Schreibe einen Wert auf einen digitalen Pin.
    :param pin: Der Pin, auf den geschrieben werden soll (Pyfirmata Pin-Objekt)
    :param value: Der Wert, der geschrieben werden soll (0 oder 1)
    """
    pin.write(value)

def read_analog_pin(pin):
    """
    Lese den Wert eines analogen Pins.
    :param pin: Der Pin, der gelesen werden soll (Pyfirmata Pin-Objekt)
    :return: Der Wert des Pins (0.0 bis 1.0)
    """
    return pin.read()

# Beispielprojekte:




# 1. LED Blinken:
print("LED Blinken Beispiel")
start = input("Start?")
for _ in range(5):  # Blinke 5 Mal
    
    write_digital_pin(led_pin, 1)  # LED an
    time.sleep(1)
    write_digital_pin(led_pin, 0)  # LED aus
    time.sleep(1)







# 2. Taster Status prüfen:
print("Taster Status prüfen Beispiel")
start = input("Start?")
for _ in range(10):  # Überprüfe 10 Mal
    start = input("Read?")
    button_state = read_digital_pin(button_pin)
    if button_state:
        print("Button gedrückt")
    else:
        print("Button nicht gedrückt")
    time.sleep(0.5)






# 3. Analoger Sensorwert lesen:
print("Analoger Sensorwert lesen Beispiel")
start = input("Start?")
for _ in range(10):  # Lese 10 Mal
    start = input("Read?")
    sensor_value = read_analog_pin(sensor_pin)
    if sensor_value is not None:
        print(f'Sensorwert: {sensor_value:.2f}')
    else:
        print("Sensorwert ist None")
    time.sleep(1)





# Abschluss:
print("Beispielcode abgeschlossen")
