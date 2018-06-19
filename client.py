import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCDLib
import time
import math
lcd = LCDLib.Adafruit_CharLCDBackpack()
lcd.set_backlight(0)
max_len = 5
row_pins = [13,14,15,16]
col_pins = [19,20,21]
color_pins = [18,23]
txt = ""
start_time = time.time()

def elapsed():
    return time.time() - start_time

appears = False
def update():
    global appears
    needs_update = False
    #print(math.floor(elapsed()) % 2)
    msg = "ID: " + txt
    if elapsed() % 1 < 0.5 and not appears:
        #lcd.clear()
        appears = True
        needs_update = True
    elif elapsed() % 1 >= 0.5 and appears:
        #lcd.clear()
        appears = False
        needs_update = True
    if needs_update:
        lcd.clear()
        lcd.message("ID: " + txt + ("|" if appears else ""))# + "\nYour message here.")
def press(id):
    if id == 10:
        submit()
        return
    if len(txt) > 0 and id == 12:
        txt = txt[:-1]
    if len(txt) <= max_len:
        if id < 10:
            txt += str(id)
        elif id == 11:
            txt += "0"

GPIO.setmode(GPIO.BCM)
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
            print(str(GPIO.input(cp)) + " " + str(rp) + ", " + str(cp))
            if GPIO.input(cp):
                if not buttons_pressed[button_id]:
                    buttons_pressed[button_id] = True
                    press(button_id)
                else:
                    buttons_pressed[button_id] = False
            update()
GPIO.cleanup()
