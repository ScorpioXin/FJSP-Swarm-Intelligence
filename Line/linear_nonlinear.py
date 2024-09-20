import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib
import matplotlib.ticker as ticker

matplotlib.use('TkAgg')

# 定义函数
def f(x, y):
    return -(x**2+y**2)


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

ax.scatter(0, 0, color='red', marker='o', s=300)
ax.text(2, 2, 4, "优化目标", fontsize=22, fontname='Simsun', fontweight='bold')

# 设置坐标轴标签
ax.set_xlabel('x', fontname='Times New Roman', fontsize=35)
ax.set_ylabel('y', fontname='Times New Roman', fontsize=35)
ax.set_zlabel('z', fontname='Times New Roman', fontsize=35)
ax.xaxis.labelpad = 10    # 与坐标轴的距离
ax.yaxis.labelpad = 10
ax.zaxis.labelpad = 10
plt.tick_params(labelsize=20)


# 应用刻度标签格式化函数到坐标轴
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
ax.xaxis.set_major_locator(MaxNLocator(integer=True, steps=[5]))

ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
ax.yaxis.set_major_locator(MaxNLocator(integer=True, steps=[5]))
ax.zaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
ax.zaxis.set_major_locator(MaxNLocator(integer=True, steps=[5]))


# 直线
# fig, ax = plt.subplots()
# plt.rcParams['font.sans-serif'] = ['SimSun']
# w = x = np.linspace(0, 20, 1000)
# f = 1/2*w
# for spine in ax.spines.values():
#     spine.set_linewidth(2)  # 设置边框粗细
# ax.plot(w, f, linewidth=6)
# ax.set_xlabel('x', fontname='Times New Roman', fontsize=60)
# ax.xaxis.set_major_locator(MaxNLocator(integer=True, steps=[4]))
# ax.set_ylabel('y', fontname='Times New Roman', fontsize=60)
# ax.yaxis.set_major_locator(MaxNLocator(integer=True, steps=[2]))
# plt.tick_params(direction='in')
# plt.tick_params(labelsize=45)
# ax.scatter(20, 10, color='red', marker='o', s=500)
# ax.text(16, 9.7, "优化目标", fontsize=43, fontname='Simsun', fontweight='bold')

ax = plt.gca()
width = 2
ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
ax.spines['bottom'].set_linewidth(width)
ax.spines['left'].set_linewidth(width)
ax.spines['right'].set_linewidth(width)
plt.show()
plt.show()