import Jetson.GPIO as GPIO
import subprocess
import serial
import time

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

#配置串口
ser = serial.Serial('/dev/ttyTHS1', 115200)


# 设置GPIO引脚为输入模式
# GPIO.setup(pin1, GPIO.IN)
# GPIO.setup(pin2, GPIO.IN)

subprocess.run(['python3','/home/liu/Code/B/position.py'])

subprocess.run(['python3', '/home/liu/Code/B/1.py'])
time.sleep(10)

subprocess.run(['python3', '/home/liu/Code/B/2.py'])
time.sleep(10)


subprocess.run(['python3', '/home/liu/Code/B/34.py'])

