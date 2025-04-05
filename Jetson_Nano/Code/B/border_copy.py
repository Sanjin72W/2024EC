import cv2
import numpy as np
import math
import serial
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

	#smin = 160 * 105 = 16800
	#smax = 300 * 195 = 58500
	#拟合后四个端点


	#轮廓逼近
	epsilon = 0.02 * cv2.arcLength(contour, True)  # 设置逼近的精度
	approx_contour = cv2.approxPolyDP(contour, epsilon, True)
	#判断凸凹
	is_convex = cv2.isContourConvex(contour)

	# 计算近似后的轮廓的边界框
	x, y, w, h = cv2.boundingRect(contour)
	
	# 计算宽高比例
	aspect_ratio = w / h
	if (len(approx_contour) != 4) or (cv2.contourArea(contour) > 58500) or (cv2.contourArea(contour) < 16800) :
		return False
	else:
		return True





cv2.namedWindow("Tracking",cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
cv2.createTrackbar("x1", "Tracking", 0, 640, nothing)
cv2.createTrackbar("y1", "Tracking", 0, 480, nothing)
cv2.createTrackbar("x2", "Tracking", 640, 640, nothing)
cv2.createTrackbar("y2", "Tracking", 480, 480, nothing)


# 初始化摄像头
cap = cv2.VideoCapture('/dev/video0')  # 0代表默认摄像头，根据实际情况进行调整

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

	# 二值化处理
	_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU) #通过otsu方法选定阈值

	# 开运算处理
	open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
	binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN,open_kernel)
	
	#闭运算处理
	open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
	binary = cv2.morphologyEx(binary,cv2.MORPH_CLOSE,None)


	# 反相处理
	inverted = cv2.bitwise_not(binary)

	# 寻找轮廓
	contours,hierarchy= cv2.findContours(inverted, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	print("现在轮廓数：",format(len(contours)))

	#创建用来存储特殊矩形的列表
	A4contours = []

	for contour in contours:
	# 调用函数来检验轮廓
		if similar_to_rectangle(contour):
			# 如果函数返回 True，将轮廓添加到 A4contours 列表中
			A4contours.append(contour)

	print(len(A4contours))
	
	# for contour in A4contours:
	# 	cv2.drawContours(frame, [contour], 0, (255, 255, 255), 1)

	if len(A4contours) != 2:
		print("轮廓不合法")

	else:
		incontour = max(A4contours, key=cv2.contourArea)
		outcontour = min(A4contours,key=cv2.contourArea)
		#内轮廓逼近
		epsilon = 0.02 * cv2.arcLength(incontour, True)  # 设置逼近的精度
		approx_incontour = cv2.approxPolyDP(incontour, epsilon, True)

		#外轮廓逼近
		epsilon = 0.02 * cv2.arcLength(outcontour, True)  # 设置逼近的精度
		approx_outcontour = cv2.approxPolyDP(outcontour, epsilon, True)


		#保证轮廓合法
		if len(approx_incontour) !=4 | len(approx_outcontour) != 4: 
			print("轮廓不合法")
			pass
		else:
			#重新排序轮廓端点的位置
			inpoints = sort_rectangle_points(approx_incontour)
			outpoints = sort_rectangle_points(approx_outcontour)

			#再次确认轮廓合法
			if (not inpoints) | (not outpoints):
				print("轮廓不合法")
				pass
			else:
				#打印输出内外轮廓端点
				for point in inpoints:
					x, y = point[0]
					print("Point in coordinates: x={}, y={}".format(x, y))
					pass
				for point in outpoints:
					x, y = point[0]
					print("Point out coordinates: x={}, y={}".format(x, y))
					pass

				#得到轨道中线矩形的轮廓
				midpoints = np.zeros_like(outpoints)
				for i in range(4):
					midpoints[i] = (inpoints[i] + outpoints[i])/2 
				
				#打印中心线到画面
				cv2.drawContours(frame, [midpoints], 0, (255, 255, 255), 1)
				pass

	#显示画面
	cv2.imshow('1',inverted)
	cv2.imshow('real',frame)

	#按ESC终止
	key = cv2.waitKey(1)
	if key == 27:  # Esc
		break

cv2.destroyAllWindows()