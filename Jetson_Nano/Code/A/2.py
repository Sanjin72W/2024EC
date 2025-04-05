import serial
import time
import cv2
import numpy as np

capture = cv2.VideoCapture('/dev/video0')
ser=serial.Serial('/dev/ttyTHS1',115200,timeout=1) #使用U串行口
while(True):
    ret, RGB1 = capture.read()
    RGB = cv2.flip(RGB1, 1)  # 镜像
    # 把RGB转换为HSV格式
    HSV = cv2.cvtColor(RGB, cv2.COLOR_BGR2HSV)
    # cv2.imshow('HSV',HSV)

    # 选定所判断颜色的阈值
    minRed = np.array([160, 100, 50])
    maxRed = np.array([180, 255, 255])

    mask = cv2.inRange(HSV, minRed, maxRed)
    red = cv2.bitwise_and(RGB, RGB, mask=mask)
    cv2.imshow('red',mask)


    # 闭运算
    n = np.ones((10, 10), np.uint8)
    close1 = cv2.morphologyEx(red, cv2.MORPH_CLOSE, n, iterations=5)
    cv2.imshow('close1', close1)

    # 开运算
    k = np.ones((12, 12), np.uint8)
    open1 = cv2.morphologyEx(close1, cv2.MORPH_OPEN, k)
    cv2.imshow('open1',open1)



    gray = cv2.cvtColor(open1, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150)
    cv2.imshow('edge',edges)
    # 第一个参数是单通道图片，只能是二值图
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 判断是否找到轮廓
    if len(contours) == 0:
        # 处理轮廓为空的情况
        print("未找到轮廓。")

    else:
        max_contour = contours[0]  # 初始化最大轮廓为第一个轮廓
        print(len(contours))
        for contour in contours:
            for point in contour:
                x, y = point[0]
                print("Point coordinates: x={}, y={}".format(x, y))
        max_area = cv2.contourArea(contours[0])  # 初始化最大面积为第一个轮廓的面积

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour
        x, y, w, h = cv2.boundingRect(max_contour)
        brcnt = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
        cv2.drawContours(RGB, [brcnt], -1, (0, 255, 0), 3)        

        # 确定中心坐标
        global X,Y
        X = ((2 * x) + w) / 2
        Y = ((2 * y) + h) / 2

        RGB = cv2.circle(RGB, (int(X), int(Y)), 15, (0, 255, 0), -1)
#        RGB = cv2.circle(RGB, (320, 240), 15, (0, 255, 0), -1)


        #print(RGB.shape)#获取视频高度和宽度，确定中心点，（320，240）
        if(abs(320-int(X))>25 and abs(240-int(Y))>32):#如果在边角
            if((320-int(X))<0 and (240-int(Y))<0):#右下
                myinput = bytes([0xAB])
                ser.write(myinput)  # 向端口数据
                time.sleep(0.1)
            elif ((320 - int(X)) > 0 and (240 - int(Y)) < 0):#左下
                myinput = bytes([0xBB])
                ser.write(myinput)  # 向端口数据
                time.sleep(0.1)
            elif ((320 - int(X)) < 0 and (240 - int(Y)) > 0):
                myinput = bytes([0xAA])
                ser.write(myinput)  # 向端口数据
                time.sleep(0.1)
            elif ((320 - int(X)) > 0 and (240 - int(Y)) > 0):
                myinput = bytes([0xBA])
                ser.write(myinput)  # 向端口数据
                time.sleep(0.1)
        elif (abs(320 - int(X)) > 25 and abs(240 - int(Y)) < 32):#如果在水平方向
            if ((320 - int(X)) < 0):#右
                myinput = bytes([0xAC])
                ser.write(myinput)  # 向端口数据
                time.sleep(0.1)
            if ((320 - int(X)) > 0):#左
                myinput = bytes([0xBC])
                ser.write(myinput)  # 向端口数据
                time.sleep(0.1)
        elif (abs(320 - int(X)) < 25 and abs(240 - int(Y)) > 32):#如果在垂直方向
            if ((240 - int(Y)) < 0):#下
                myinput = bytes([0xCB])
                ser.write(myinput)  # 向端口数据
                time.sleep(0.1)
            if ((240 - int(Y)) > 0):#上
                myinput = bytes([0xCA])
                ser.write(myinput)  # 向端口数据
                time.sleep(0.1)

    cv2.imshow("video", RGB)
    if cv2.waitKey(1) == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()







