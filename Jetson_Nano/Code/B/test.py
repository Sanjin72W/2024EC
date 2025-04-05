import cv2
import numpy as np
import serial
import time

# cap = cv2.VideoCapture("/dev/video0")
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ser = serial.Serial('/dev/ttyTHS1', 115200)

#将数字转换为发送的字符的函数
def format_number(num):
    abs_num = abs(num)
    formatted_num = f"{abs_num}"
    return formatted_num

def nothing():
	pass


# cv2.namedWindow("Tracking",cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
# cv2.createTrackbar("ELH", "Tracking", 170, 180, nothing)
# cv2.createTrackbar("ELS", "Tracking", 40, 255, nothing)
# cv2.createTrackbar("ELV", "Tracking", 117, 255, nothing)
# cv2.createTrackbar("LH", "Tracking", 0, 180, nothing)
# cv2.createTrackbar("LS", "Tracking", 42, 255, nothing)
# cv2.createTrackbar("LV", "Tracking", 81, 255, nothing)
# cv2.createTrackbar("UH", "Tracking", 10, 180, nothing)
# cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
# cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)
# cv2.createTrackbar("BIN", "Tracking", 0, 255, nothing)

# while True:
# 	# 读取图片
# 	_, frame = cap.read()
# 	# 压缩图像
# 	frame=cv2.resize(frame,(640,480))

# 	el_h = cv2.getTrackbarPos("ELH", "Tracking")
# 	el_s = cv2.getTrackbarPos("ELS", "Tracking")
# 	el_v = cv2.getTrackbarPos("ELV", "Tracking")

# 	l_h = cv2.getTrackbarPos("LH", "Tracking")
# 	l_s = cv2.getTrackbarPos("LS", "Tracking")
# 	l_v = cv2.getTrackbarPos("LV", "Tracking")

# 	u_h = cv2.getTrackbarPos("UH", "Tracking")
# 	u_s = cv2.getTrackbarPos("US", "Tracking")
# 	u_v = cv2.getTrackbarPos("UV", "Tracking")
# 	bina = cv2.getTrackbarPos("BIN", "Tracking")

# 	#转hsv
# 	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# 	#上下限设定
# 	l_g = np.array([l_h, l_s, l_v])  # lower green value
# 	u_g = np.array([u_h, u_s, u_v])
# 	el_g = np.array([el_h,el_s,el_v])
# 	eu_g = np.array([180,255,255])

# 	#取范围
# 	mask = cv2.inRange(hsv, l_g, u_g) + cv2.inRange(hsv,el_g,eu_g)

# 	cv2.imshow("1",mask)
# 	# # 开运算处理
# 	# open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# 	# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,open_kernel)

# 	#闭运算处理
# 	close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
# 	mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,close_kernel)

# 	#轮廓识别
# 	contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 	# 查找最大的轮廓
# 	if len(contours) > 0:
# 		largest_contour = max(contours, key=cv2.contourArea)

# 		#找到光斑中心点
# 		x, y, w, h = cv2.boundingRect(largest_contour)
# 		X = ((2 * x) + w) / 2
# 		Y = ((2 * y) + h) / 2

# 		X = int(X)
# 		Y = int(Y)
		#打印输出：
# for i in range(10):


      
data ="#"+format_number(127)+"$"+format_number(127)+"%"+"127"+"^"+"127"

print("发送：",data)

ser.write((data+"\n").encode())

time.sleep(0.005)


# received_data = []


data = ser.read(2)  # 一次读取100个字节的数据


# received_data.append(data)



# # 将列表中的数据合并成一个字节串（bytes类型）
# received_bytes = b''.join(received_data)

print(data)
# # # else:
	# # 	print("无可用轮廓")


# 	#取出目标图像
# 	res = cv2.bitwise_and(frame, frame, mask = mask)  # src1,src2

# 	cv2.imshow("frame", frame)
# 	cv2.imshow("mask", mask)
# 	cv2.imshow("out", res)

# 	key = cv2.waitKey(1)
# 	if key == 27:  # Esc
# 		break

# cv2.destroyAllWindows()

