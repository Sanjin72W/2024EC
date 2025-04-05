import matplotlib.pyplot as plt

# 示例数据
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# 创建折线图
plt.plot(x, y, label='折线图', marker='o', linestyle='-', color='b')

# 添加图表标题和标签
plt.title('简单折线图示例')
plt.xlabel('X轴数据')
plt.ylabel('Y轴数据')

# 添加图例
plt.legend()

# 显示图表
plt.show()
