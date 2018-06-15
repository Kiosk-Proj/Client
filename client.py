import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCDLib
lcd = LCDLib.Adafruit_CharLCDBackpack()
lcd.set_backlight(0)
max_len = 5
row_pins = [13,14,15,16]
col_pins = [19,20,21]
color_pins = [18,23]
txt = ""

def press(id):
    if id == 10:
        submit()
    if len(txt) > 0 and id == 12:
        txt = txt[:-1]
    if len(txt) <= max_len:
        if id < 10:
            txt += str(id)
        elif id == 11:
            txt += "0"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(row_pins, GPIO.OUT)
GPIO.setup(color_pins, GPIO.OUT)
GPIO.setup(col_pins, GPIO.IN)
GPIO.output(row_pins, GPIO.LOW)
buttons_pressed = [False] * 12
while True:
    button_id = 0
    for rp in row_pins:
        GPIO.output(rp, GPIO.HIGH)
        for cp in col_pins:
            button_id += 1
            if GPIO.input(cp)
                if not buttons_pressed[button_id]:
                    buttons_pressed[button_id] = True
                    press(button_id)
                else:
                    buttons_pressed[button_id] = False

GPIO.cleanup()
