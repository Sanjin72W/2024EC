import serial
import time
import cv2
import numpy as np

capture = cv2.VideoCapture('/dev/video0')
ser=serial.Serial('/dev/ttyTHS1',115200,timeout=1) #使用USB连接串行口
while(True):
    ret, RGB1 = capture.read()
    RGB = cv2.flip(RGB1, 1)  # 镜像
    # 把RGB转换为HSV格式
    HSV = cv2.cvtColor(RGB, cv2.COLOR_BGR2HSV)
    # cv2.imshow('HSV',HSV)

    # 选定所判断颜色的阈值
    minRed = np.array([160, 100, 130])
    maxRed = np.array([180, 255, 255])

    mask = cv2.inRange(HSV, minRed, maxRed)
    red = cv2.bitwise_and(RGB, RGB, mask=mask)
    cv2.imshow('red',red)

    # 开运算
    k = np.ones((12, 12), np.uint8)
    open1 = cv2.morphologyEx(red, cv2.MORPH_OPEN, k)
    # cv2.imshow('open1',open1)


    # 闭运算
    n = np.ones((10, 10), np.uint8)
    close1 = cv2.morphologyEx(open1, cv2.MORPH_CLOSE, n, iterations=5)
    cv2.imshow('close1', close1)


    gray = cv2.cvtColor(close1, cv2.COLOR_BGR2GRAY)
    # 第一个参数是单通道图片，只能是灰度图或者二值图
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST)

    # 判断是否找到轮廓
    if contours == []:
        cv2.imshow("video", RGB)
        c = cv2.waitKey(1)
    else:
        a = len(contours)
        for i in range(a):
            if cv2.contourArea(contours[i]) > cv2.contourArea(contours[0]):
                contours[0] = contours[i]

        x, y, w, h = cv2.boundingRect(contours[0])
        brcnt = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
        cv2.drawContours(RGB, [brcnt], -1, (0, 255, 0), 3)
        # cv2.imshow("result",RGB)

        # 确定中心坐标
        global X,Y
        X = ((2 * x) + w) / 2
        Y = ((2 * y) + h) / 2

        RGB = cv2.circle(RGB, (int(X), int(Y)), 15, (0, 255, 0), -1)
#        RGB = cv2.circle(RGB, (320, 240), 15, (0, 255, 0), -1)

        cv2.imshow("video", RGB)

     
        c = cv2.waitKey(1)
    if c == 27:
        break







