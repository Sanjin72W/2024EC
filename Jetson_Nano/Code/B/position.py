import cv2
import numpy as np
import serial
import time
import math
import Jetson.GPIO as GPIO

ledde_pin = 33
ledok_pin = 32

# GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledde_pin, GPIO.OUT)
GPIO.setup(ledok_pin, GPIO.OUT)

#配置串口
ser = serial.Serial('/dev/ttyTHS1', 115200)

#将数字转换为发送的字符的函数
def format_number(num):
	abs_num = abs(num)
	formatted_num = f"{abs_num}"
	return formatted_num

#空函数
def nothing():
	pass

def sort_rectangle_points(points):
	# 计算四个点的中心坐标（重心）
	center_x = sum(point[0][0] for point in points) / 4
	center_y = sum(point[0][1] for point in points) / 4

	# 计算每个点相对于重心的角度
	angles = []
	for point in points:
		x = point[0][0]
		y = point[0][1]
		angle = np.arctan2(y - center_y, x - center_x)
		angles.append(angle)

	# 根据角度进行排序
	sorted_indices = sorted(range(len(points)), key=lambda i: angles[i])

	# 返回排序后的四个点坐标
	sorted_points = [points[i] for i in sorted_indices]
	return sorted_points


def similar_to_rectangle(contour):

	# smin = 320 * 320 
	# smax = 430 * 430 
	#拟合后四个端点
	smin = 102400
	smax = 184900


	#轮廓逼近
	epsilon = 0.03 * cv2.arcLength(contour, True)  # 设置逼近的精度
	approx_contour = cv2.approxPolyDP(contour, epsilon, True)


	if (len(approx_contour) != 4) or (cv2.contourArea(contour)>smax) or (cv2.contourArea(contour)<smin):
		return False
	else:
		return True

#摄像头初始化
cap = cv2.VideoCapture("/dev/video0")
# cap.set(cv2.CAP_PROP_FPS, 24)

#中心点偏差值
xl = 260
xr = 380
yu = 200
yd = 310

conuter = 0

while True:
# 读取摄像头画面
	ret, frame = cap.read()
	if not ret:
		break
	
	# 转换为灰度图像
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#增强对比
	clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(5, 5))
	gray = clahe.apply(gray)

	# 边缘检测
	binary = cv2.Canny(gray, 50, 150, apertureSize=3)
	# cv2.imshow("8",binary)
	
	#闭运算处理
	close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	binary = cv2.morphologyEx(binary,cv2.MORPH_CLOSE,close_kernel)
	cv2.imshow("edge1",binary)

	#轮廓识别
	contours,hierarchy= cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#创建用来存储特殊矩形的列表
	A4contours = []

	for contour in contours:
	# 调用函数来检验轮廓
		if similar_to_rectangle(contour):
			# 如果函数返回 True，将轮廓添加到 A4contours 列表中
			A4contours.append(contour)

	if len(A4contours) == 0:
		print("无有效轮廓")
		GPIO.output(ledde_pin,GPIO.HIGH)
		conuter = 0
		pass
	else:
		#找到最大轮廓
		largest_contour = max(contours, key=cv2.contourArea)

		#轮廓逼近多边形
		epsilon = 0.02 * cv2.arcLength(largest_contour, True)  # 设置逼近的精度
		approx_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

		#多边形画线
		cv2.drawContours(frame, [approx_contour], 0, (255, 255, 255), 1)
		if len(approx_contour) != 4: 
			print("轮廓不合法")
			GPIO.output(ledde_pin,GPIO.HIGH)
			conuter = 0
			pass
		else:
			#重新排序轮廓端点的位置
			points = sort_rectangle_points(approx_contour)

			#再次确认轮廓合法
			if (not points) :
				print("轮廓不合法")
				GPIO.output(ledde_pin,GPIO.HIGH)
				conuter = 0
				pass
			else:
				x = sum(p[0][0] for p in points)/4
				y = sum(p[0][1] for p in points)/4
				print("Point: x={}, y={}".format(x, y))
				if x>xr or x<xl or y<yu or y>yd:
					GPIO.output(ledde_pin,GPIO.HIGH)
					print("未复位")
					time.sleep(0.2) 
					contour = 0
				else:
					GPIO.output(ledde_pin,GPIO.LOW)
					print("已复位")
					time.sleep(0.2)
					conuter += 1
	
	if conuter == 10:
		GPIO.output(ledok_pin,GPIO.HIGH)
		time.sleep(5)
		GPIO.output(ledok_pin,GPIO.LOW)
		break

	#调节识别间隔的时间
	key = cv2.waitKey(1)
	if key == 27:  # Esc
		break

cv2.destroyAllWindows()
