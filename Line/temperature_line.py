import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')

# 作温度函数的曲线图
def WLine(Ts, Tmax, alpha, beta, delta):

    t = np.arange(0, Tmax + 0.1, 0.1)
    tm = max(t)
    # 指数降温
    T_exponent = [Ts*(alpha**tn) for tn in t]

    # 快速降温
    T_fast = [Ts/(1+beta*tn) for tn in t]

    # 多普勒降温
    T_Doppler = [abs( Ts*(delta**tn) * np.cos(tm*0.05*(1-tn/tm)) + np.cos((1-tn/tm)) ) for tn in t]
    # T_Doppler = [abs(Ts * (delta**tn) * (1+np.sin(-5 * tn/Ts)) * np.cos((-5 * tn/Ts))) for tn in t]

    # 绘制曲线
    plt.plot(t, T_exponent, color='red', label='指数型降温', linewidth=4)
    plt.plot(t, T_fast, color='green', label='快速型降温', linewidth=4)
    plt.plot(t, T_Doppler, color='blue', label='多普勒型降温', linewidth=4)

    # 设置全局字体及大小
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 35

    # 添加标题和标签
    # plt.title('惯性权重W变换曲线')
    plt.xlabel('迭代次数', size=35)
    plt.ylabel('温度', size=35)
    plt.xticks(np.arange(0, Tmax + 1, 50))
    plt.yticks(np.arange(0, Ts + 10, 20))
    plt.tick_params(labelsize=35)           # 刻度标签的字体大小
    plt.tick_params(direction='in')         # 指定刻度线的方向
    plt.legend(loc='upper right')
    # plt.grid(True)

    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)

    # 显示图形
    plt.show()

if __name__ == "__main__":
    WLine(200, 500, 0.99, 0.5, 0.99)