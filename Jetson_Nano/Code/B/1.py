import cv2
import numpy as np
import serial
import time
import math

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


# 获取坐标的函数
def get_actual_distance(frame):

	#读取参数
	el_h = cv2.getTrackbarPos("ELH", "Tracking")
	el_s = cv2.getTrackbarPos("ELS", "Tracking")
	el_v = cv2.getTrackbarPos("ELV", "Tracking")

	l_h = cv2.getTrackbarPos("LH", "Tracking")
	l_s = cv2.getTrackbarPos("LS", "Tracking")
	l_v = cv2.getTrackbarPos("LV", "Tracking")

	u_h = cv2.getTrackbarPos("UH", "Tracking")
	u_s = cv2.getTrackbarPos("US", "Tracking")
	u_v = cv2.getTrackbarPos("UV", "Tracking")

	#转hsv
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#上下限设定
	l_g = np.array([l_h, l_s, l_v])  
	u_g = np.array([u_h, u_s, u_v])
	el_g = np.array([el_h,el_s,el_v])
	eu_g = np.array([180,255,255])

	#取范围
	mask = cv2.inRange(hsv, l_g, u_g) + cv2.inRange(hsv,el_g,eu_g)

	# # 开运算处理
	# open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,open_kernel)

	#闭运算处理
	close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
	mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,close_kernel)

	#轮廓识别
	contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# 查找最大的轮廓
	if len(contours) > 0:
		largest_contour = max(contours, key=cv2.contourArea)

		#找到光斑中心点
		x, y, w, h = cv2.boundingRect(largest_contour)
		X = ((2 * x) + w) / 2
		Y = ((2 * y) + h) / 2

		X = int(X)
		Y = int(Y)	
		return (X,Y)
	else:
		return False

def similar_to_rectangle(contour):

	# smin = 320 * 320 
	# smax = 430 * 430 
	smin = 102400
	smax = 184900
	#拟合后四个端点


	#轮廓逼近
	epsilon = 0.03 * cv2.arcLength(contour, True)  # 设置逼近的精度
	approx_contour = cv2.approxPolyDP(contour, epsilon, True)


	if (len(approx_contour) != 4) or (cv2.contourArea(contour)>smax) or (cv2.contourArea(contour)<smin):
		return False
	else:
		return True

#创建参数条
cv2.namedWindow("Tracking",cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
cv2.createTrackbar("ELH", "Tracking", 170, 180, nothing)
cv2.createTrackbar("ELS", "Tracking", 60, 255, nothing)
cv2.createTrackbar("ELV", "Tracking", 140, 255, nothing)

cv2.createTrackbar("LH", "Tracking", 0, 180, nothing)
cv2.createTrackbar("LS", "Tracking", 60, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 140, 255, nothing)

cv2.createTrackbar("UH", "Tracking", 10, 180, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

cv2.createTrackbar("x1", "Tracking", 0, 640, nothing)
cv2.createTrackbar("y1", "Tracking", 0, 480, nothing)
cv2.createTrackbar("x2", "Tracking", 640, 640, nothing)
cv2.createTrackbar("y2", "Tracking", 480, 480, nothing)



#摄像头初始化
cap = cv2.VideoCapture("/dev/video0")
# cap.set(cv2.CAP_PROP_FPS, 24)

#初始化接受数据
received_data = []

while True:
# 读取摄像头画面
	ret, frame = cap.read()
	if not ret:
		break

	#裁切摄像头画面
	x1 = cv2.getTrackbarPos("x1", "Tracking")
	y1 = cv2.getTrackbarPos("y1", "Tracking")
	x2 = cv2.getTrackbarPos("x2", "Tracking")
	y2 = cv2.getTrackbarPos("y2", "Tracking")

	frame =frame[y1:y2, x1:x2]

	
	# 转换为灰度图像
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#增强对比
	clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(5, 5))
	gray = clahe.apply(gray)

	# 边缘检测
	binary = cv2.Canny(gray, 120, 150, apertureSize=3)
	cv2.imshow("8",binary)

	# lines =[]
	
	# lines = cv2.HoughLinesP(binary, rho=1, theta=math.pi / 180, threshold=20, minLineLength=7, maxLineGap=5)


	# if lines is None:
	# 	print("识别失败")
	# else:
	# 	# 遍历找到的直线
	# 	for line in lines:
	# 		x1, y1, x2, y2 = line[0]  # 提取直线的起点和终点坐标

	# 		# 绘制拟合后的直线到原始图像
	# 		# cv2.line(binary, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)

	# 	cv2.imshow("2",binary)
		
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
			pass
		else:
			#重新排序轮廓端点的位置
			points = sort_rectangle_points(approx_contour)

			#再次确认轮廓合法
			if (not points) :
				print("轮廓不合法")
				pass
			else:
				#获取激光位置
				actual_position = get_actual_distance(frame)
				#判断是否识别成功
				if (not actual_position):
					#失败则继续运行，重新识别
					print("Point now not find")
					pass
				else:
					#开始操控
					#延时

					# time.sleep(0.5)

					#获取
					x = sum(p[0][0] for p in points)/4
					y = sum(p[0][1] for p in points)/4

					#初始为未到达，循环等待到达
					reach = False

					while not reach:
						ret, RGB = cap.read()
						if not ret:
							break		
						#获取激光位置
						actual_position = get_actual_distance(RGB)	
						if not actual_position:
							#打印输出轮廓端点和现在坐标
							print("Point to: x={}, y={}".format(x, y))
							print("Point not find")
							pass
							
						else:
							#打印输出轮廓端点和现在坐标
							print("Point to: x={}, y={}".format(x, y))
							print("Point now: x={},y={}".format(actual_position[0],actual_position[1]))

							#误差设置
							systematic_error_x = 0
							systematic_error_y = 0
							Accidental_error_x = 10
							Accidental_error_y = 10

							#发送坐标
							data ="#"+format_number(actual_position[0])+"$"+format_number(actual_position[1])+"%"+format_number(int(x))+"^"+format_number(int(y))
							print("Send: ",data)
							ser.write((data+"\n").encode())
							
							if abs(actual_position[0]-systematic_error_x-x)<=Accidental_error_x and abs(actual_position[1]-y-systematic_error_y)<=Accidental_error_y:
								reach = True
								pass
							
							time.sleep(0.005)

						#到达后发送下一个坐标值
					#到达最后一个点后退出
					for i in range(100):
						data ="#"+format_number(127)+"$"+format_number(127)+"%"+format_number(127)+"^"+format_number(127)
						print("Send: ",data)
						ser.write((data+"\n").encode())
						time.sleep(0.01)
					break
					#成功
	cv2.imshow("edge",binary)
	cv2.imshow("Image with Hough Lines", frame)

	#调节识别间隔的时间
	key = cv2.waitKey(1)
	if key == 27:  # Esc
		break


	
cv2.destroyAllWindows()
