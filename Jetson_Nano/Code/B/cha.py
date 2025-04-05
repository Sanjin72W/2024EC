import numpy as np
from shapely.geometry import Polygon, LinearRing
from shapely.ops import orient

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

# 示例输入：四边形的端点坐标（根据提供的轮廓信息）
points = [np.array([[137, 81]], dtype=np.int32), np.array([[487, 93]], dtype=np.int32), 
          np.array([[519, 448]], dtype=np.int32), np.array([[97, 442]], dtype=np.int32)]
num_divisions = 9

# 调用函数生成新的轮廓点列表
new_contour = add_divisions_to_quad(points, num_divisions)

# 打印新的轮廓点列表
print(new_contour)
