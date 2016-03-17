#!/usr/bin/python

import RPi.GPIO as GPIO
from lib.Adafruit_PWM_Servo_Driver import PWM
from lib import xbox_read
import time
import math

# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=True)							#connects to breakout board address 0x40 in debug mode
pwm2 = PWM(0x41, debug = True)
# Default calibration values
#32768 max range in xbox controller analog stick / 255 for triggers


move = 0
move2 = 500									#used for pwm signal max value
servoMin = 500 									#used for min value for drive servos
servoMove = 150 								#used for min value for camera servos
servoMoveBasket = 400 								#used for min value for basket servos
servoMoveArm = 400								#used for min values for arm servos
menu = 1 									#used to toggle between camera servos and capture carry servos
pwm.setPWMFreq(50) 
pwm2.setPWMFreq(2000)                    						# Set frequency to 50 Hz


#main loop
while(True):
	for event in xbox_read.event_stream(deadzone=6000):			#looks for a button to be pressed sets deadzone (sensitivity) to 6000
		if(event.key == 'Y1' and event.value > 0):			#moves drive servos based on degree of analog stick movement
			move =  4003 - (3500 * event.value)/32768 
			pwm2.setPWM(0,servoMin,move)	
		if(event.key == 'Y1' and event.value < 0):
			move = 4004 - (3500 * -event.value)/32768
			pwm2.setPWM(2,servoMin,move)
		if(event.key == 'Y1' and event.value == 0):
			servoMin = 500
			pwm2.setPWM(0,servoMin,move)
			pwm2.setPWM(2,servoMin,move)
		if(event.key == 'Y2' and event.value > 0):
			move =  4003 - (3500 * event.value)/32768 
			pwm2.setPWM(1,servoMin,move) 
		if(event.key == 'Y2' and event.value < 0):
			move = 4004 - (3500 * -event.value)/32768
			pwm2.setPWM(3,servoMin,move)
		if(event.key == 'Y2' and event.value == 0):
			servoMin = 500
			pwm2.setPWM(1,servoMin,move)
			pwm2.setPWM(3,servoMin,move)
		if(event.key == 'du' and event.value == 1 and servoMin == 500):	#gives fine control of drive motor movement when analog sticks not being used
			move = move +100
			print(move)
			#servoMin = 0
			#pwm.setPWM(0,servoMin,move)
			#pwm.setPWM(1,servoMin,move)
			#pwm.setPWM(2,servoMin,move)
			#pwm.setPWM(3,servoMin,move)
			#time.sleep(.05)
			#servoMin = 500
			#pwm.setPWM(0,servoMin,move)
			#pwm.setPWM(1,servoMin,move)
			#pwm.setPWM(2,servoMin,move)
			#pwm.setPWM(3,servoMin,move)
		if(event.key == 'dd' and event.value == 1 and servoMin == 500):
			move = move -100
			print(move)
			#servoMin = 490
			#pwm.setPWM(0,servoMin,move)
			#pwm.setPWM(1,servoMin,move)
			#pwm.setPWM(2,servoMin,move)
			#pwm.setPWM(3,servoMin,move)
			#time.sleep(.05)
			servoMin = 500
			pwm.setPWM(0,servoMin,move)
			pwm.setPWM(1,servoMin,move)
			pwm.setPWM(2,servoMin,move)
			pwm.setPWM(3,servoMin,move)
		if(event.key == 'dr' and event.value == 1 and servoMin == 500):
			freq = freq + 500
			pwm.setPWMFreq(freq)
			print(freq)
			#servoMin = 0
			#pwm.setPWM(2,servoMin,move)
			#pwm.setPWM(3,servoMin,move)
			#time.sleep(.05)
			#servoMin = 500
			#pwm.setPWM(2,servoMin,move)
			#pwm.setPWM(3,servoMin,move)
		if(event.key == 'dl' and event.value == 1 and servoMin == 500):
			freq = freq - 500
			pwm.setPWMFreq(freq)
			print(freq)
			#servoMin = 0
			#pwm.setPWM(0,servoMin,move)
			#pwm.setPWM(1,servoMin,move)
			#time.sleep(.05)
			#servoMin = 500
			#pwm.setPWM(0,servoMin,move)
			#pwm.setPWM(1,servoMin,move)
		if(event.key == 'LT'):						#gives control of camera servos based on trigger movement
			if(menu == 1):								#also gives control of cature carry system based on trigger position
				if(servoMove < 350):
					servoMove = servoMove + 5
					pwm.setPWM(4,servoMove,move2)
			if(menu == 2): 
				servoMoveArm =  400 - (400 * event.value)/255 
				pwm.setPWM(4,servoMoveArm,move2)
		if(event.key == 'RT'):
			if(menu == 1):
				if(servoMove > 0):
					servoMove = servoMove - 5
					pwm.setPWM(4,servoMove,move2)
			if(menu == 2):
				servoMoveBasket =  400 - (400 * event.value)/255
				pwm.setPWM(4,servoMoveBasket,move2)		
		if(event.key == 'A' and event.value == 1 and servoMoveArm == 400 and servoMoveBasket == 400): #toggles the function of the trigger buttons with capture carry safeguard 
			if(menu == 1):
				menu = 2
			elif(menu == 2):
				menu = 1
		if(event.key == 'B' and event.value == 1):			#reset mechanism in case safety mechanism fails
			servoMoveArm = servoMoveBasket = 400

		
        
