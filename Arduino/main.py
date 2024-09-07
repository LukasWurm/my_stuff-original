import pyfirmata
import time

# Ersetze 'COM4' durch den richtigen Port deines Arduinos
board = pyfirmata.Arduino('COM4')

# Start der Kommunikation zwischen Python und Arduino
it = pyfirmata.util.Iterator(board)
it.start()

# Definiere einen Pin als Ausgang
pin = board.get_pin('d:5:o')

# LED blinken lassen
for i in range(5):
    pin.write(1)  # Pin auf HIGH setzen (LED einschalten)
    time.sleep(1)
    pin.write(0)  # Pin auf LOW setzen (LED ausschalten)
    time.sleep(1)
