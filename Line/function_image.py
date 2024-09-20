import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator

matplotlib.use('TkAgg')

# 定义函数
def f(x, y):
    return (x**2+y**2) - abs(1.5*x*y)
    # return abs(x**2 + y**3) - (x+y)**2 - y

# 创建数据
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# 绘制图像
fig = plt.figure()
plt.rcParams['font.sans-serif'] = ['SimSun']
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

# 设置坐标轴标签
ax.set_xlabel('x', fontname='Times New Roman', fontsize=30)
ax.set_ylabel('y', fontname='Times New Roman', fontsize=30)
ax.set_zlabel('f (x,y)', fontname='Times New Roman', fontsize=30)
ax.xaxis.labelpad = 10    # 与坐标轴的距离
ax.yaxis.labelpad = 10
ax.zaxis.labelpad = 10
plt.tick_params(labelsize=20)

# 应用刻度标签格式化函数到坐标轴
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
ax.zaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
ax.zaxis.set_major_locator(MaxNLocator(integer=True, steps=[5]))

# 显示图像
plt.show()
