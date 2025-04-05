import cv2
import numpy as np

def similar_to_rectangle(contour):

    #定义与A4纸相同的矩形
    rect = np.array([[0, 0], [1414, 0], [1414, 100], [0, 100]])

    # 计算轮廓的边界框
    contour_box = cv2.boundingRect(contour)

    # 计算矩形的边界框
    rect_box = cv2.boundingRect(rect)

    # 计算边界框之间的相似性（均方差）
    mse = np.mean((np.array(contour_box) - np.array(rect_box)) ** 2)

    # 设置一个相似性阈值，判断是否相似
    mse_threshold = 100
    if mse < mse_threshold:
        return True
    else:
        return False

# 示例调用
image = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)
_, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# 查找轮廓
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 定义一个矩形
rect = np.array([[100, 100], [300, 100], [300, 300], [100, 300]])

# 判断第一个轮廓是否与矩形相似
# result = compare_contour_to_rectangle(contours[0], rect)
print(result)
