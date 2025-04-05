import cv2
import numpy as np
import serial
import time
import math

def nothing():
	pass

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
		return X,Y,mask
	else:
		return False
	
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


#摄像头初始化
cap = cv2.VideoCapture("/dev/video0")
# cap.set(cv2.CAP_PROP_FPS, 24)

while True:
# 读取摄像头画面
	ret, frame = cap.read()
	if not ret:
		break

	# frame =frame[y1:y2, x1:x2]
	if not get_actual_distance :
		print("未识别到轮廓")
	else:
		X,Y,mask=get_actual_distance(frame)
		print("Point now: x={},y={}".format(X,Y))

	cv2.imshow("frame", frame)
	cv2.imshow("mask", mask)
	#调节识别间隔的时间
	key = cv2.waitKey(1)
	if key == 27:  # Esc
		break

cv2.destroyAllWindows()