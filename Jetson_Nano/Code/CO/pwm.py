import Jetson.GPIO as GPIO
import time

led1_pin = 32  # 使用支持PWM的引脚
led2_pin = 33
a = 7
b = 11
c = 13
d = 15
frequency = 20000  # 1 kHz的PWM频率

# 设置GPIO模式为BOARD
GPIO.setmode(GPIO.BOARD)

# 设置GPIO引脚为输出模式
GPIO.setup(led1_pin, GPIO.OUT)
GPIO.setup(led2_pin, GPIO.OUT)
GPIO.setup(a, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
GPIO.setup(c, GPIO.OUT)
GPIO.setup(d, GPIO.OUT)


# 创建或获取PWM对象
if hasattr(GPIO, 'pwm'):
	GPIO.PWM.stop()

pwm1 = GPIO.PWM(led1_pin, frequency)
pwm2 = GPIO.PWM(led2_pin, frequency)

GPIO.output(a,GPIO.HIGH)
GPIO.output(b,GPIO.HIGH)
GPIO.output(c,GPIO.LOW)
GPIO.output(d,GPIO.LOW)

duty = 50
try:
	while True:
		
		pwm1.start(duty)
		pwm2.start(duty)
		print(1)
		time.sleep(2)



except KeyboardInterrupt:
	# 如果用户中断程序（按下Ctrl+C），进行清理并退出
	pwm1.stop()
	pwm2.stop()

	GPIO.cleanup()
	print("\n程序结束。")
