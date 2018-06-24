import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCDLib
import math
import time

lcd = LCDLib.Adafruit_CharLCDBackpack()
lcd.set_backlight(0)
max_len = 4
row_pins = [13,12,6,16]
col_pins = [19,20,21]
color_pins = [18,23]
txt = ""

def send_to_server():
	return

def reset():
	global txt
	txt = ""
	print("RESETTING")
	lcd.set_cursor(0,1)
	lcd.message("             ")
	lcd.home()
	lcd.message("ID:      ")
	lcd.set_cursor(4, 0)
	return

def submit():
	lcd.set_cursor(0,1)
	lcd.message("Are you sure?")
	GPIO.output(row_pins[3], GPIO.HIGH)

	time.sleep(1)	
	while True:
		if(GPIO.input(col_pins[0])):
			lcd.set_cursor(0, 1)
			lcd.message("             ")
			lcd.set_cursor(4+len(txt), 0)
			
			while True:
				if(not GPIO.input(col_pins[0])):
			 		return
		elif(GPIO.input(col_pins[2])):
			send_to_server()
			reset()
			return
		

appears = False
def press(id):

    global txt
    if id == 12 and len(txt) == 5:
        submit()
        return
    if len(txt) > 0 and id == 10:
        txt = txt[:-1]
        lcd.set_cursor(4 + len(txt), 0)
        lcd.message(" ")
        lcd.set_cursor(4 + len(txt), 0)
    if len(txt) <= max_len:
        if id < 10:
            txt += str(id)
            lcd.message(str(id))
        elif id == 11:
            txt += "0"
            lcd.message("0")

GPIO.setmode(GPIO.BCM)
GPIO.setup(row_pins, GPIO.OUT)
GPIO.setup(color_pins, GPIO.OUT)
GPIO.setup(col_pins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN	)
GPIO.output(row_pins, GPIO.LOW)
buttons_pressed = [False] * 12
pressing = False
current = -1

#Set up LCD
lcd.show_cursor(True)
lcd.home()
lcd.message("ID: ")


while True:
    button_id = 0
    for rp in row_pins:
        GPIO.output(rp, GPIO.HIGH)
        for cp in col_pins:
            button_id += 1
            print(str(button_id) + " " + str(GPIO.input(cp)) + " " + str(rp) + ", " + str(cp))            
            current = GPIO.input(cp)
            if current and not buttons_pressed[button_id - 1]:
                buttons_pressed[button_id - 1] = True            
                press(button_id)
            elif not current and buttons_pressed[button_id - 1]:
                buttons_pressed[button_id - 1] = False
            
#if GPIO.input(cp):
            #    if not pressing:
            #        pressing = True
            #        current = button_id
            #        press(button_id)
            #elif GPIO.input(cp) and not button_id==current: 
            #    pressing = True
            #else:
            #   pressing = False
             #   current = -1
            #update()
        GPIO.output(rp, GPIO.LOW)
GPIO.cleanup()
