import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCDLib
import math
import time
import random
import connection
from subprocess import call	

#lcd = LCDLib.Adafruit_CharLCDBackpack()
#print("Initalized lcd library")
#lcd.set_backlight(0)
max_len = 4
row_pins = [16,6,12,13] 
col_pins = [19,20,21]
color_pins = [18,23]
txt = ""
button_id = 0

#lcd.message("ID: ")
server_ip = "96.225.21.203"
server_port = 25565
#server_connection = connection.Connection(server_ip,server_port)
#server_connection.connect()

color_dict = {
        "white": 0,
        "hotpink": 1,
        "yellow": 2,
        "red": 3,
        "babyblue": 4,
        "darkblue": 5,
        "green": 6,
        "null": 7
}

def set_color(color):
	#really high iq stuff with bitwise operators
    port1 = color & 0b1
    port0 = (color >> 1) & 0b1
    back = (color >> 2) & 0b1
    GPIO.output(color_pins[1], port1)
    GPIO.output(color_pins[0], port0)
    lcd.set_backlight(back)

def send_to_server():
	#replaces bottom text with Checking and waits for a response from the server
	#lcd.set_cursor(0,1)
	#lcd.message("Checking...  ")
	print("checking")	
	#sends
	#print(myConnection.send(Message(MessageType.CONNECTION, 0, b'/00/00')))
	#response = myConnection.message_protocol(Message(MessageType.INPUT, 0, 12598))	
	'''
	#shuts down if given id 99999
	#probably not going to be used, just an idea for how to shutdown the pi without disconnecting the power
	#a button on the inside of the kiosk is probably a better option
	if(txt == "99999"):
		set_color(2)
		lcd.set_cursor(0, 1)
		lcd.message("Shutting Down...     ")
		#safely close connection with server
		call(["sudo", "shutdown", "now"])
	'''
	
	
##	if(response.transactionID != -1):
##		set_color(color_dict['green'])
##		lcd.set_cursor(0,1)
##		name = response.messageValue[4:][1::2].decode('utf-8')
##		lcd.message('ID is invalid 	\n' + name)
##	else:
##		set_color(color_dict['red'])
##		lcd.set_cursor(0,1)
##		lcd.message("ID is invalid			")
	
	#sets the color back to normal	
##	time.sleep(.5)
##	set_color(color_dict['null'])
##	return

def reset():
	#resets all variables and the LCD display for the next user
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

	#waits for a second enter or delete press
	time.sleep(0.25)	
	while True:
		#if delete is pressed get rid of the message on line 2 and return to id input
		if(GPIO.input(col_pins[0])):
			lcd.set_cursor(0, 1)
			lcd.message("             ")
			lcd.set_cursor(4+len(txt), 0)
			
			#waits until delete is released to return to id input so that no number is deleted
			while True:
				if(not GPIO.input(col_pins[0])):
			 		return
	 #if enter is pressed send to the server and reset
		elif(GPIO.input(col_pins[2])):
			send_to_server()
			reset()
			return
		

appears = False
def press(id):
    global txt
    print(txt)    
    #if enter is pressed and submit the id
    if id == 12 and len(txt) == 5:
		print("submitted: " + txt)
		#submit()
		return
    #if delete is pressed remove one number from input and txt
    if len(txt) > 0 and id == 10:
        txt = txt[:-1]
        #lcd.set_cursor(4 + len(txt), 0)
        #lcd.message(" ")
        #lcd.set_cursor(4 + len(txt), 0)
    #only allow input if there are less than 5 numbers in the input field    
    if len(txt) <= max_len:
    	#if any of the number keys save 0 are pressed add them to the text and display them
        if id < 10:
            txt += str(id)
            #lcd.message(str(id))
        #if zero is pressed add zero to the input field and txt
        elif id == 11:
            txt += "0"
            #lcd.message("0")
    
GPIO.setmode(GPIO.BCM) 
GPIO.setup(row_pins, GPIO.OUT)
GPIO.setup(color_pins, GPIO.OUT)
GPIO.setup(col_pins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN	)
GPIO.output(row_pins, GPIO.LOW)

buttons_pressed = [False] * 12
pressing = False
current = -1

#Set up LCD
#lcd.show_cursor(True)
#lcd.home()
#lcd.message("ID: ")

#set_color(7)

while True:
    button_id = 0
    for rp in row_pins:
        GPIO.output(rp,GPIO.HIGH)
        for cp in col_pins:
                button_id += 1
                current = GPIO.input(cp)
                if current and not buttons_pressed[button_id  - 1]:
                        buttons_pressed[button_id - 1] = True
                        press(button_id)
                elif not current and buttons_pressed[button_id - 1]:
                        buttons_pressed[button_id - 1] = False 
        GPIO.output(rp, GPIO.LOW)
GPIO.cleanup()