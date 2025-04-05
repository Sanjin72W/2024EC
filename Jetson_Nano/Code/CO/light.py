import Jetson.GPIO as GPIO
import time
import sys
import cv2

led_pin = 33

# GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)


try:

	while 1:
		print('on')
		GPIO.output(led_pin,GPIO.HIGH)
		time.sleep(0.5)
		print('off')
		GPIO.output(led_pin,GPIO.LOW)
		time.sleep(0.5)

except KeyboardInterrupt:
	GPIO.output(led_pin,GPIO.LOW)
	GPIO.cleanup()
	
print('done')

