import Jetson.GPIO as GPIO
import keyboard
import time


GPIO.setwarnings(False)

# 使用支持PWM的引脚
right_pwm = 33
left_pwm = 32 

# 配置控制引脚
right_pin1 = 7
right_pin2 = 11
left_pin1 = 13
left_pin2 = 15
frequency = 20000 # 20 kHz的PWM频率

# 设置GPIO模式为BOARD
GPIO.setmode(GPIO.BOARD)

# 设置GPIO引脚为输出模式
GPIO.setup(left_pwm, GPIO.OUT)
GPIO.setup(right_pwm, GPIO.OUT)
GPIO.setup(left_pin1, GPIO.OUT)
GPIO.setup(left_pin2, GPIO.OUT)
GPIO.setup(right_pin1, GPIO.OUT)
GPIO.setup(right_pin2, GPIO.OUT)

speedl = speedr = 45 #初始化速度
#实验室地面40左右
#循迹地面45左右

# 创建PWM对象并初始化
if hasattr(GPIO, 'pwm'):
	GPIO.PWM.stop()
pwml = GPIO.PWM(left_pwm, frequency)
pwmr = GPIO.PWM(right_pwm, frequency)
pwml.start(speedl)
pwmr.start(speedr)

try:
	while 1:
		if keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
			if not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
				pwml.ChangeDutyCycle(speedl)
				pwmr.ChangeDutyCycle(speedr)
				GPIO.output(left_pin1,GPIO.HIGH)
				GPIO.output(left_pin2,GPIO.LOW)
				GPIO.output(right_pin1,GPIO.HIGH)
				GPIO.output(right_pin2,GPIO.LOW)
				time.sleep(0.05) 
			elif keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
				pwml.ChangeDutyCycle(speedl)
				pwmr.ChangeDutyCycle(speedr)
				GPIO.output(left_pin1,GPIO.LOW)
				GPIO.output(left_pin2,GPIO.HIGH)
				GPIO.output(right_pin1,GPIO.HIGH)
				GPIO.output(right_pin2,GPIO.LOW)
				time.sleep(0.05) 				
			elif not keyboard.is_pressed('a') and keyboard.is_pressed('d'):
				pwml.ChangeDutyCycle(speedl)
				pwmr.ChangeDutyCycle(speedr)
				GPIO.output(left_pin1,GPIO.HIGH)
				GPIO.output(left_pin2,GPIO.LOW)
				GPIO.output(right_pin1,GPIO.LOW)
				GPIO.output(right_pin2,GPIO.HIGH)
				time.sleep(0.05)
			elif keyboard.is_pressed('a') and keyboard.is_pressed('d'):
				pwml.ChangeDutyCycle(speedl)
				pwmr.ChangeDutyCycle(speedr)
				GPIO.output(left_pin1,GPIO.HIGH)
				GPIO.output(left_pin2,GPIO.LOW)
				GPIO.output(right_pin1,GPIO.HIGH)
				GPIO.output(right_pin2,GPIO.LOW)
				time.sleep(0.05) 
		elif not keyboard.is_pressed('w') and keyboard.is_pressed('s'):
			if not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
				pwml.ChangeDutyCycle(speedl)
				pwmr.ChangeDutyCycle(speedr)
				GPIO.output(left_pin1,GPIO.LOW)
				GPIO.output(left_pin2,GPIO.HIGH)
				GPIO.output(right_pin1,GPIO.LOW)
				GPIO.output(right_pin2,GPIO.HIGH)
				time.sleep(0.05) 
			elif keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
				pwml.ChangeDutyCycle(speedl)
				pwmr.ChangeDutyCycle(speedr)
				GPIO.output(left_pin1,GPIO.HIGH)
				GPIO.output(left_pin2,GPIO.LOW)
				GPIO.output(right_pin1,GPIO.LOW)
				GPIO.output(right_pin2,GPIO.HIGH)
				time.sleep(0.05) 			
			elif not keyboard.is_pressed('a') and keyboard.is_pressed('d'):
				pwml.ChangeDutyCycle(speedl)
				pwmr.ChangeDutyCycle(speedr)
				GPIO.output(left_pin1,GPIO.LOW)
				GPIO.output(left_pin2,GPIO.HIGH)
				GPIO.output(right_pin1,GPIO.LOW)
				GPIO.output(right_pin2,GPIO.LOW)
				time.sleep(0.05)
			elif keyboard.is_pressed('a') and keyboard.is_pressed('d'):
				pwml.ChangeDutyCycle(speedl)
				pwmr.ChangeDutyCycle(speedr)
				GPIO.output(left_pin1,GPIO.LOW)
				GPIO.output(left_pin2,GPIO.HIGH)
				GPIO.output(right_pin1,GPIO.LOW)
				GPIO.output(right_pin2,GPIO.HIGH)
				time.sleep(0.05) 
		elif keyboard.is_pressed('w') and keyboard.is_pressed('s'):
			pwml.ChangeDutyCycle(0)
			pwmr.ChangeDutyCycle(0)
			GPIO.output(left_pin1,GPIO.LOW)
			GPIO.output(left_pin2,GPIO.LOW)
			GPIO.output(right_pin1,GPIO.LOW)
			GPIO.output(right_pin2,GPIO.LOW)
			time.sleep(0.05) 	
		elif not keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
			pwml.ChangeDutyCycle(0)
			pwmr.ChangeDutyCycle(0)
			GPIO.output(left_pin1,GPIO.LOW)
			GPIO.output(left_pin2,GPIO.LOW)
			GPIO.output(right_pin1,GPIO.LOW)
			GPIO.output(right_pin2,GPIO.LOW)
			time.sleep(0.05) 
		if keyboard.is_pressed('z') and not keyboard.is_pressed('q'):
			if speedl >= 10:
				speedl -= 10
			elif speedl <10:
				pass
		elif not keyboard.is_pressed('z') and keyboard.is_pressed('q'):
			if speedl <= 90:
				speedl += 10
			elif speedl >90:
				pass
		if keyboard.is_pressed('c') and not keyboard.is_pressed('e'):
			if speedr >= 10:
				speedr -= 10
			elif speedr <10:
				pass
		elif not keyboard.is_pressed('c') and keyboard.is_pressed('e'):
			if speedr <= 90:
				speedr += 10
			elif speedr >90:
				pass	
		
except KeyboardInterrupt:
	# 如果用户中断程序（按下Ctrl+C），进行清理并退出
	pwml.stop()
	pwmr.stop()

	GPIO.cleanup()
	print("\n程序结束。")
