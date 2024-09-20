import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt

# 定义函数
def function(v):
    return 1/(1+np.exp(-v))

v = np.linspace(-10, 10, 1000)
y = function(v)

plt.rcParams['font.sans-serif'] = ['SimSun']
fig, ax = plt.subplots()
ax.plot(v, y, color='blue', linewidth=5)

# 设置坐标轴零点
plt.xlabel('粒子速度', size=35)
plt.ylabel('映射函数值', size=35)
plt.xticks(np.arange(-10, 10 + 1, 2), fontname='Times New Roman')
plt.yticks(np.arange(0, 1.1, 0.2), fontname='Times New Roman')
plt.tick_params(labelsize=35)  # 刻度标签的字体大小
plt.tick_params(direction='in')  # 指定刻度线的方向

ax = plt.gca()
width = 2
ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
ax.spines['bottom'].set_linewidth(width)
ax.spines['left'].set_linewidth(width)
ax.spines['right'].set_linewidth(width)

# 显示图形
plt.show()


