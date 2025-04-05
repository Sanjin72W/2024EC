import cv2
import numpy as np
from simple_pid import PID
import serial

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

#坐标排序函数
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

#创建参数条
cv2.namedWindow("Tracking",cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
cv2.createTrackbar("ELH", "Tracking", 170, 180, nothing)
cv2.createTrackbar("ELS", "Tracking", 40, 255, nothing)
cv2.createTrackbar("ELV", "Tracking", 117, 255, nothing)

cv2.createTrackbar("LH", "Tracking", 0, 180, nothing)
cv2.createTrackbar("LS", "Tracking", 42, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 81, 255, nothing)

cv2.createTrackbar("UH", "Tracking", 10, 180, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

cv2.createTrackbar("x1", "Tracking", 0, 640, nothing)
cv2.createTrackbar("y1", "Tracking", 0, 480, nothing)
cv2.createTrackbar("x2", "Tracking", 640, 640, nothing)
cv2.createTrackbar("y2", "Tracking", 480, 480, nothing)






# 获取实际距离的函数
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
	l_g = np.array([l_h, l_s, l_v])  # lower green value
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

#摄像头初始化
cap = cv2.VideoCapture("/dev/video0")
cap.set(cv2.CAP_PROP_FPS, 24)

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
	clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
	gray = clahe.apply(gray)

	# 边缘检测
	edges = cv2.Canny(gray, 50, 150, apertureSize=3)

	cv2.imshow("2",edges)

	#闭运算处理
	close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
	binary = cv2.morphologyEx(edges,cv2.MORPH_CLOSE,close_kernel)

	#轮廓识别
	contours,hierarchy= cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) == 0:
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
				#打印输出内外轮廓端点
				for point in points:

					#计算中心点坐标
					x_mid = sum(p[0][0] for p in points)/4
					y_mid = sum(p[0][1] for p in points)/4

					#打印中心点
					print("Point in coordinates: x={}, y={}".format(x_mid, y_mid))
					
					# 目标坐标
					setx = x_mid 
					sety = y_mid 


					actual_distance = get_actual_distance(frame)

					if (not actual_distance):
						controlx_signal = 0
						controly_signal = 0
						print("无可用激光点")
					else:

						print(actual_distance[0])
						print(actual_distance[1])

						controlx_signal = - int(pidx(actual_distance[0]))
						controly_signal = - int(pidy(actual_distance[1]))

						data ="#"+"0"+"$"+"0"+"%"+format_number(controlx_signal)+"^"+format_number(controly_signal)
						print("发送：",data)
						ser.write((data+"\n").encode())

	cv2.imshow("edge",binary)
	cv2.imshow("Image with Hough Lines", frame)
	key = cv2.waitKey(100)
	if key == 27:  # Esc
		break

cv2.destroyAllWindows()
