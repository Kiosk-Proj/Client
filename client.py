import RPi.GPIO as GPIO
row_pins = [13,14,15,16]
col_pins = [17,18,19]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(row_pins, GPIO.OUT)
GPIO.setup(col_pins, GPIO.IN)
