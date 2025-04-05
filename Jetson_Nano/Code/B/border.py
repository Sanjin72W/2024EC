import cv2
import numpy as np
import math
import serial

def nothing():
	pass

def sort_rectangle_points(points):
	# 计算四个点的横坐标之和和纵坐标之和
	x_sum = sum(p[0][0] for p in points)
	y_sum = sum(p[0][1] for p in points)

	# 计算四个点的横坐标和纵坐标的差值
	x_diff = [p[0][0] - x_sum / 4 for p in points]
	y_diff = [p[0][1] - y_sum / 4 for p in points]

	# 排序并返回结果
	sorted_points = [points[i] for i in sorted(range(len(points)), key=lambda i: (y_diff[i], x_diff[i]))]
	
	#再次确认轮廓合法
	if len(sorted_points) != 4:
		return False
	else:
		#交换次序，保证顺序
		change = sorted_points[2]
		sorted_points[2] = sorted_points[3]
		sorted_points[3] = change

		#返回结果
		return sorted_points
	

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
	open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
	binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN,open_kernel)
	
	#闭运算处理
	open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
	binary = cv2.morphologyEx(binary,cv2.MORPH_CLOSE,None)


	# 反相处理
	inverted = cv2.bitwise_not(binary)

	# 寻找轮廓
	contours,hierarchy= cv2.findContours(inverted, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	
	#判断是否正常识别
	if len(contours) != 2:
		print("未识别到有效轮廓，现在轮廓数：",format(len(contours)))
		pass
	else:
		#分别存储内外轮廓
		if hierarchy[0][0][3]==-1:
			incontour = contours[1]
			outcontour = contours[0]
		else:
			incontour = contours[0]
			outcontour = contours[1]


		# 对边框轮廓进行逼近，得到近似的边框轮廓

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