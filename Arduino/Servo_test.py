import pyfirmata
import time

# Arduino-Board initialisieren (Ändere den Port entsprechend deinem Setup)
board = pyfirmata.Arduino('COM4')  # Beispiel für Windows: 'COM3', für Linux: '/dev/ttyUSB0'

# Analog-Pin definieren (z.B. A0)
analog_pin = board.get_pin('a:0:i')

# PWM-Pin definieren (z.B. D6)
pwm_pin = board.get_pin('d:6:p')

# Servo-Pin definieren (z.B. D11)
servo_pin = board.get_pin('d:11:s')

# Iterator starten, um sicherzustellen, dass kontinuierlich analoge Daten gelesen werden
it = pyfirmata.util.Iterator(board)
it.start()

# Setze die Servoposition auf eine Anfangsposition (z.B. 90 Grad)
servo_pin.write(90)

try:
    while True:
        # Lese den analogen Wert
        analog_value = analog_pin.read()
        
        if analog_value is not None:
            # Drucke den analogen Wert
            print(f"Analog Value: {analog_value}")
            
            # Skaliere den analogen Wert für das PWM-Signal (0-1)
            pwm_value = analog_value
            pwm_pin.write(pwm_value)
            
            # Skaliere den analogen Wert für die Servoposition (0-180 Grad)
            servo_angle = analog_value * 180
            servo_pin.write(servo_angle)
        
        # Warte einen kurzen Moment
        time.sleep(0.1)

except KeyboardInterrupt:
    # Beende das Programm bei einer Tastatureingabe (z.B. STRG + C)
    print("Programm wird beendet")
finally:
    # Schließe die Verbindung zum Board
    board.exit()
