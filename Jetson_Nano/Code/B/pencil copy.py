import cv2
import numpy as np

def hough_line_detection(image):
	return image

cap = cv2.VideoCapture("/dev/video0")
cap.set(cv2.CAP_PROP_FPS, 24)
while True:
# 读取摄像头画面
	ret, frame = cap.read()
	if not ret:
		break
	# x1, y1 = 100, 10  # 左上角坐标
	# x2, y2 = 540, 450  # 右下角坐标	
	# frame =frame[y1:y2, x1:x2]
	# 转换为灰度图像
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#对比度增加
	clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(8, 8))
	gray = clahe.apply(gray)
	cv2.imshow("compare",gray)
	
	# 边缘检测
	gray = cv2.Canny(gray, 5, 150, apertureSize=3)
	cv2.imshow("edg",gray)

	#中值滤波
	gray = cv2.medianBlur(gray, 3)  
	cv2.imshow("mid",gray)

	#闭运算处理
	close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
	gray = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,close_kernel)	
	cv2.imshow("close",gray)


	# 开运算处理
	open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN,open_kernel)
	cv2.imshow("open",gray)


	#轮廓识别
	contours,hierarchy= cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) == 0:
		print("无有效轮廓")
	else:

		#找到最大轮廓
		largest_contour = max(contours, key=cv2.contourArea)

		#轮廓逼近多边形
		epsilon = 0.02 * cv2.arcLength(largest_contour, True)  # 设置逼近的精度
		approx_incontour = cv2.approxPolyDP(largest_contour, epsilon, True)
		cv2.drawContours(frame, [approx_incontour], 0, (255, 255, 255), 1)


		# # 进行霍夫直线检测
		# lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

		# # 绘制检测到的直线b
		# if lines is not None:
		# 	for line in lines:
		# 		rho, theta = line[0]
		# 		a = np.cos(theta)
		# 		b = np.sin(theta)
		# 		x0 = a * rho
		# 		y0 = b * rho
		# 		x1 = int(x0 + 1000 * (-b))
		# 		y1 = int(y0 + 1000 * (a))
		# 		x2 = int(x0 - 1000 * (-b))
		# 		y2 = int(y0 - 1000 * (a))
		# 		cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

	cv2.imshow("edge",gray)
	cv2.imshow("Image with Hough Lines", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
