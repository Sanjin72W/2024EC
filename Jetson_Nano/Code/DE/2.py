"""
# File       : mask_check.py
# Time       ：2021/6/10 15:02
# Author     ：Meng
# version    ：python 3.10
# Description：
"""
import cv2          # 导入opencv
import time         # 导入time

"""实现鼻子检测"""
def nose_dection(img):
	img = cv2.GaussianBlur(img,(5,5),0)#高斯滤波
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                     # 将图片转化成灰度
	nose_cascade = cv2.CascadeClassifier('/home/liu/Code/DE/haarcascades/haarcascade_mcs_nose.xml')
	# nose_cascade.load("haarcascades/haarcascade_mcs_nose.xml")  # 文件所在的具体位置
	'''此文件是opencv的haar鼻子特征分类器'''
	noses = nose_cascade.detectMultiScale(gray, 1.3, 5)  # 鼻子检测
	for(x,y,w,h) in noses:
		cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 画框标识鼻子
	flag = 0            # 检测到鼻子的标志位，如果监测到鼻子，则判断未带口罩
	if len(noses)>0:
		flag = 1
	return img,flag

""""实现眼睛检测"""
def eye_dection(img):
	img = cv2.GaussianBlur(img,(5,5),0)#高斯滤波
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                     # 将图片转化成灰度
	eyes_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
	# eyes_cascade.load("haarcascades/haarcascade_eye_tree_eyeglasses.xml")  # 文件所在的具体位置
	'''此文件是opencv的haar眼睛特征分类器'''
	eyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)          # 眼睛检测
	for (x,y,w,h) in eyes:
		frame = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)  # 画框标识眼部
		print("x y w h is",(x,y,w,h))
		# frame = cv2.rectangle(img, (x, y+h), (x + 3*w, y + 3*h), (255, 0, 0), 2)  # 画框标识眼部
	return img,eyes

def empty(a):
	pass

def main():
	# image = cv2.imread("1.png")      # 读取背景照片
	# cv2.imshow('skin', image)                       # 展示
	# cv2.createTrackbar("Hmin", "skin", 0, 90, empty)    # 创建bar
	# cv2.createTrackbar("Hmax", "skin", 25, 90, empty)
	capture=cv2.VideoCapture('/dev/video0')               # 打开摄像头，其中0为自带摄像头，
	while True:
		ref,img=capture.read()                  # 打开摄像头
		# img = cv2.imread("./images/train_301.jpg")      # 读取一张图片
		img_hsv = img
		image_nose,flag_nose = nose_dection(img)       # 进行口罩检测，返回检测之后的图形以及标志位
		if flag_nose == 1:              # 当检测到鼻子的时候，判断未戴口罩
			frame = cv2.putText(image_nose, "NO MASK", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.9,(0, 0, 255), 1)  # 在图片上写字
			cv2.imshow('img', image_nose)       # 展示图片
		if flag_nose == 0:              # 未检测鼻子，进行眼睛检测
			img_eye,eyes = eye_dection(img)         # 进行眼睛检测，返回检测之后的图形以及标志位
			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)        # 将图片转化成HSV格式
			H, S, V = cv2.split(hsv)                          #
			Hmin= cv2.getTrackbarPos("Hmin", 'skin')           # 获取bar
			Hmax= cv2.getTrackbarPos("Hmax", 'skin')
			if Hmin> Hmax:
				Hmax= Hmin
			thresh_h = cv2.inRange(H, Hmin, Hmax)       # 提取人体肤色区域
			if len(eyes) > 1:                           # 判断是否检测到两个眼睛，其中eyes[0]为左眼坐标
				# 口罩区域的提取
				mask_x_begin = min(eyes[0][0],eyes[1][0])               # 把左眼的x坐标作为口罩区域起始x坐标
				mask_x_end = max(eyes[0][0],eyes[1][0]) + eyes[list([eyes[0][0], eyes[1][0]]).index(max(list([eyes[0][0], eyes[1][0]])))][2]   # 把右眼x坐标 + 右眼宽度作为口罩区域x的终止坐标
				mask_y_begin = max(eyes[0][1] + eyes[0][3],eyes[1][1] + eyes[1][3]) + 20    # 把眼睛高度最大的作为口罩区域起始y坐标
				if mask_y_begin > img_eye.shape[1]:     # 判断是否出界
					mask_y_begin = img_eye.shape[1]
				mask_y_end = max(eyes[0][1] + 3 * eyes[0][3],eyes[1][1] + 3 * eyes[1][3]) + 20  # 同理
				if mask_y_end > img_eye.shape[1]:
					mask_y_end = img_eye.shape[1]
				frame = cv2.rectangle(img_eye, (mask_x_begin, mask_y_begin), (mask_x_end, mask_y_end), (255, 0, 0), 2)  # 画口罩区域的框
				total_mask_pixel = 0
				total_face_pixel = 0
				# 遍历二值图，为0则total_mask_pixel+1，否则total_face_pixel+1
				for i in range(mask_x_begin,mask_x_end):
					for j in range(mask_y_begin,mask_y_end):
						if thresh_h[i,j] == 0:
							total_mask_pixel += 1
						else:
							total_face_pixel += 1
				print("total_mask_pixel",total_mask_pixel)
				print("total_face_pixel", total_face_pixel)
				if total_mask_pixel > total_face_pixel:
					frame = cv2.putText(img_eye, "HAVE MASK", (mask_x_begin, mask_y_begin - 10),cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 255), 1)  # 绘制
				if total_mask_pixel < total_face_pixel:
					frame = cv2.putText(img_eye, "NO MASK", (mask_x_begin, mask_y_begin - 10), cv2.FONT_HERSHEY_COMPLEX,0.9, (0, 0, 255), 1)  # 绘制
			cv2.imshow("skin", thresh_h)  # 显示肤色图
			cv2.imshow("img", img_eye)  #`su,t5ycc` 显示肤色图
			# cv2.imwrite('005_result.jpg',img_eye)     保存图片
		c = cv2.waitKey(10)
		if c==27:
			break
	capture.release()       #
	cv2.destroyAllWindows() # 关闭所有窗口


if __name__ == '__main__':
	main()
