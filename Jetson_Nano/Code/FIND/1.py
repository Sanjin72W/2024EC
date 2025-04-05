import cv2
import numpy as np
# import Jetson.GPIO as GPIO
import serial


#将数字转换为发送的字符的函数
def format_number(num):
    sign = '+' if num >= 0 else '-'
    abs_num = abs(num)
    formatted_num = f"{sign}{abs_num}"
    return formatted_num

#配置串口
ser = serial.Serial('/dev/ttyTHS1', 115200)


# # 使用支持PWM的引脚 
# left_pin = 32  # Jes-32黄色接in4橙色  左轮向前
# right_pin = 33  # Jet-33蓝色接in2灰色  右轮向前
# frequency = 1000  # 1 kHz的PWM频率

# # 设置GPIO模式为BOARD
# GPIO.setmode(GPIO.BOARD)

# # 设置GPIO引脚为输出模式
# GPIO.setup(left_pin, GPIO.OUT)
# GPIO.setup(right_pin, GPIO.OUT)

# # 创建PWM对象
# if hasattr(GPIO, 'pwm'):
# 	GPIO.PWM.stop()


# pwml = GPIO.PWM(left_pin, frequency)
# pwmr = GPIO.PWM(right_pin, frequency)


# pwml.start(0)
# pwmr.start(0)

# 初始化摄像头
cap = cv2.VideoCapture('/dev/video0')  # 0代表默认摄像头，根据实际情况进行调整

try:
	while True:
	# 读取摄像头画面
		ret, frame = cap.read()
		if not ret:
			break

		# 截取路径行部分
		path_row = frame[200:280, 0:640]  # 根据实际情况调整ROI位置和大小

		# 转换为灰度图像
		gray = cv2.cvtColor(path_row, cv2.COLOR_BGR2GRAY)

		# 二值化处理
		_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU) #通过otsu方法选定阈值

		# 开运算处理
		# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
		opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN,None)
		# 反相处理
		inverted = cv2.bitwise_not(opened)

		# 寻找轮廓
		contours, _ = cv2.findContours(inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# 查找最大的黑色轮廓
		if len(contours) > 0:
			largest_contour = max(contours, key=cv2.contourArea)
			M = cv2.moments(largest_contour)
			if M["m00"] > 0:
				cx = int(M["m10"] / M["m00"])
				direct = cx - 320
				if abs(direct)>200:
					print("发送：","A")
					ser.write("A\n".encode())
				else:
					print("发送：",format_number(direct)+"\n")
					ser.write((format_number(direct)+"\n").encode())
				
	
		else:
			print("发送：","A")
			ser.write("A\n".encode())

		# cv2.imshow('1',inverted)
		

		# 检测键盘按键，按下q键退出循环
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
except KeyboardInterrupt:
	# 释放摄像头资源
	cap.release()
	cv2.destroyAllWindows()
	print("\n程序结束。")

