import cv2
import numpy as np
import serial
import time
import math

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

cv2.namedWindow("Tracking",cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
cv2.createTrackbar("x1", "Tracking", 0, 640, nothing)
cv2.createTrackbar("y1", "Tracking", 0, 480, nothing)
cv2.createTrackbar("x2", "Tracking", 640, 640, nothing)
cv2.createTrackbar("y2", "Tracking", 480, 480, nothing)



#摄像头初始化
cap = cv2.VideoCapture("/dev/video0")
# cap.set(cv2.CAP_PROP_FPS, 24)

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
	cv2.imshow("转化为灰度图像",gray)

	#增强对比
	clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
	gray = clahe.apply(gray)
	cv2.imshow("增强对比",gray)
	
	# 边缘检测
	binary = cv2.Canny(gray, 50, 150, apertureSize=3)
	cv2.imshow("边缘检测",binary)

	lines =[]
	
	lines = cv2.HoughLinesP(binary, rho=1, theta=math.pi / 180, threshold=20, minLineLength=7, maxLineGap=5)


	if lines is None:
		print("识别失败")
	else:
		# 遍历找到的直线
		for line in lines:
			x1, y1, x2, y2 = line[0]  # 提取直线的起点和终点坐标

			# 绘制拟合后的直线到原始图像
			# cv2.line(binary, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)

		# cv2.imshow("3",binary)
		
		#闭运算处理
		close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
		binary = cv2.morphologyEx(binary,cv2.MORPH_CLOSE,close_kernel)
		cv2.imshow("闭运算",binary)

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
					for point in points:
						x, y = point[0]
						print("Point to: x={}, y={}".format(x, y))

	cv2.imshow("拟合多边形并限制大小之后画框", frame)
	key = cv2.waitKey(1)
	if key == 27:  # Esc
		break

cv2.destroyAllWindows()
