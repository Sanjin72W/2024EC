import cv2
import numpy as np

cap = cv2.VideoCapture("/dev/video0")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def nothing():
	pass


cv2.namedWindow("Tracking",cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
cv2.createTrackbar("ELH", "Tracking", 0, 180, nothing)
cv2.createTrackbar("ELS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("ELV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LH", "Tracking", 0, 180, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 0, 180, nothing)
cv2.createTrackbar("US", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("BIN", "Tracking", 0, 255, nothing)

while True:
	# 读取图片
	_, frame = cap.read()
	# 压缩图像
	x1, y1 = 100, 10  # 左上角坐标
	x2, y2 = 540, 450  # 右下角坐标	
	frame =frame[y1:y2, x1:x2]

	el_h = cv2.getTrackbarPos("ELH", "Tracking")
	el_s = cv2.getTrackbarPos("ELS", "Tracking")
	el_v = cv2.getTrackbarPos("ELV", "Tracking")

	l_h = cv2.getTrackbarPos("LH", "Tracking")
	l_s = cv2.getTrackbarPos("LS", "Tracking")
	l_v = cv2.getTrackbarPos("LV", "Tracking")

	u_h = cv2.getTrackbarPos("UH", "Tracking")
	u_s = cv2.getTrackbarPos("US", "Tracking")
	u_v = cv2.getTrackbarPos("UV", "Tracking")
	bina = cv2.getTrackbarPos("BIN", "Tracking")

	#灰度化
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#对比度调整
	clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
	equalized_image = clahe.apply(gray)
	# 二值化处理
	_, binary = cv2.threshold(equalized_image, bina, 255, cv2.THRESH_BINARY) #通过otsu方法选定阈值

	# 开运算处理
	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
	opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN,None)
	# 反相处理
	inverted = cv2.bitwise_not(opened)


	#转hsv
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#上下限设定
	l_g = np.array([l_h, l_s, l_v])  # lower green value
	u_g = np.array([u_h, u_s, u_v])
	el_g = np.array([el_h,el_s,el_v])
	eu_g = np.array([180,255,255])
	mask = cv2.inRange(hsv, l_g, u_g) + cv2.inRange(hsv,el_g,eu_g)

	res = cv2.bitwise_and(frame, frame, mask = mask)  # src1,src2

	cv2.imshow("frame", frame)
	cv2.imshow("mask", mask)
	cv2.imshow("out", res)
	cv2.imshow("black",inverted)

	key = cv2.waitKey(1)
	if key == 27:  # Esc
		break

cv2.destroyAllWindows()

