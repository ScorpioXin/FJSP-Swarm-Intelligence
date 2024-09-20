import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt

# 定义函数
def function(x):
    return np.sin(x) + np.sin(2*x) + np.sin(3*x)

# 生成 x 值
x = np.linspace(-10, 10, 1000)

# 计算对应的 y 值
y = function(x)

# 创建画布和坐标轴
fig, ax = plt.subplots()

# 绘制函数曲线
ax.plot(x, y)

# 设置坐标轴零点
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# 添加标题
ax.set_title('y=sin(x)+sin(2x)+sin(3x)')

# 显示图形
plt.show()


