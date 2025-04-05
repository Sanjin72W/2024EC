import cv2
import numpy as np
import serial
import time

#配置串口
ser = serial.Serial('/dev/ttyTHS1', 115200)

#将数字转换为发送的字符的函数
def format_number(num):
	abs_num = abs(num)
	formatted_num = f"{abs_num}"
	return formatted_num

def divide_segment(p1, p2, num_divisions):
    x1, y1 = p1
    x2, y2 = p2

    # 计算两个点之间的等分点
    x_diff = (x2 - x1) / (num_divisions + 1)
    y_diff = (y2 - y1) / (num_divisions + 1)

    # 生成等分点列表
    divisions = [((int(x1 + i * x_diff), int(y1 + i * y_diff))) for i in range(1, num_divisions + 1)]

    return divisions

def add_divisions_to_quad(quad_points, num_divisions):
    if len(quad_points) != 4:
        raise ValueError("输入的 quad_points 应包含四个点。")

    # 提取四个端点的坐标
    p1 = tuple(quad_points[0][0])
    p2 = tuple(quad_points[1][0])
    p3 = tuple(quad_points[2][0])
    p4 = tuple(quad_points[3][0])

    # 生成等分点列表
    divisions_a = divide_segment(p1, p2, num_divisions)
    divisions_b = divide_segment(p2, p3, num_divisions)
    divisions_c = divide_segment(p3, p4, num_divisions)
    divisions_d = divide_segment(p4, p1, num_divisions)

    # 合并等分点和原来的端点
    new_contour = [p1] + divisions_a + [p2] + divisions_b + [p3] + divisions_c + [p4] + divisions_d + [p1]

    # 使用Shapely库进行排序，使点按顺时针排列
    # poly = Polygon(new_contour)
    # if not poly.exterior.is_ccw:
    #     poly = orient(poly, sign=1.0)

    # new_contour = np.array(poly.exterior.coords)

    return new_contour



#空函数
def nothing():
	pass

#坐标排序函数
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
	epsilon = 0.007 * cv2.arcLength(contour, True)  # 设置逼近的精度
	approx_contour = cv2.approxPolyDP(contour, epsilon, True)
	
	if (len(approx_contour) != 4) or (cv2.contourArea(contour) < 16800) or cv2.contourArea(contour) > 58500:
		return False
	else:
		return True


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

		if cv2.contourArea(largest_contour) <1:
			return False
		else:
			#找到光斑中心点
			x, y, w, h = cv2.boundingRect(largest_contour)
			X = ((2 * x) + w) / 2
			Y = ((2 * y) + h) / 2

		X = int(X)
		Y = int(Y)	
		return (X,Y)
	else:
		return False


#创建参数条
cv2.namedWindow("Tracking",cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
cv2.createTrackbar("ELH", "Tracking", 170, 180, nothing)
cv2.createTrackbar("ELS", "Tracking", 5, 255, nothing)
cv2.createTrackbar("ELV", "Tracking", 10, 255, nothing)

cv2.createTrackbar("LH", "Tracking", 0, 180, nothing)
cv2.createTrackbar("LS", "Tracking", 5, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 10, 255, nothing)

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
	cv2.imshow("二值",binary)

	# 开运算处理
	open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
	binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN,open_kernel)
	
		
	#闭运算处理
	open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
	binary = cv2.morphologyEx(binary,cv2.MORPH_CLOSE,None)

	cv2.imshow("腐蚀",binary)

	# 反相处理
	inverted = cv2.bitwise_not(binary)

	# 寻找轮廓
	contours,hierarchy= cv2.findContours(inverted, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

	#创建用来存储特殊矩形的列表
	A4contours = []

	for contour in contours:
	# 调用函数来检验轮廓
		if similar_to_rectangle(contour):
			# 如果函数返回 True，将轮廓添加到 A4contours 列表中
			A4contours.append(contour)

	print(len(A4contours))
	
	for contour in A4contours:
		cv2.drawContours(frame, [contour], 0, (255, 255, 255), 1)

	
	#判断是否正常识别
	if len(A4contours) != 2:
		print("未识别到有效轮廓，现在轮廓数：",format(len(contours)))
		pass
	else:
		#分别存储内外轮廓
		incontour = max(A4contours, key=cv2.contourArea)
		outcontour = min(A4contours,key=cv2.contourArea)
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
				#得到轨道中线矩形的轮廓
				midpoints = np.zeros_like(outpoints)
				for i in range(4):
					midpoints[i] = (inpoints[i] + outpoints[i])/2 
				
				#打印中心线到画面
				cv2.drawContours(frame, [midpoints], 0, (255, 255, 255), 1)
				pass
				#计算中心端点
				midpoints = np.zeros_like(outpoints)
				for i in range(4):
					midpoints[i] = (inpoints[i] + outpoints[i])/2 	
				
				
				#打印输出
				for point in midpoints:
					x, y = point[0]
					print("Point out coordinates: x={}, y={}".format(x, y))
					pass

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
					time.sleep(0.5)

					# 示例输入：四边形的端点坐标（根据提供的轮廓信息）
					num_divisions = 4

					# 调用函数生成新的轮廓点列表
					new_contour = add_divisions_to_quad(midpoints, num_divisions)
					
					for point in new_contour:
						x, y = point
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

								#发送坐标
								data ="#"+format_number(actual_position[0])+"$"+format_number(actual_position[1])+"%"+format_number(x)+"^"+format_number(y)
								print("Send: ",data)
								ser.write((data+"\n").encode())
								
								cv2.imshow("2", RGB)
								if abs(actual_position[0]-x)<=20 and abs(actual_position[1]-y)<=20:
									reach = True
								pass
							
							time.sleep(0.005)

							# data = ser.read(1)  # 一次读取100个字节的数据
							# received_data.append(data)
							# received_bytes = b''.join(received_data)
							# print(f"接收到的数据：{received_bytes}")

						#到达后发送下一个坐标值
					#到达最后一个点后退出
					for i in range(100):
						data ="#"+format_number(127)+"$"+format_number(127)+"%"+format_number(127)+"^"+format_number(127)
						print("Send: ",data)
						ser.write((data+"\n").encode())
						time.sleep(0.01)
					break
	cv2.imshow("edge",binary)
	cv2.imshow("Image with Hough Lines", frame)

	#调节识别间隔的时间
	key = cv2.waitKey(1)
	if key == 27:  # Esc
		break

cv2.destroyAllWindows()
