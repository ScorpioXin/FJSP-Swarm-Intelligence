import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')

# 作惯性权重的曲线图
def WLine(Wmax, Wmin, Tmax):

    t = np.arange(0, Tmax+0.1, 0.1)
    tm = max(t)
    # 线性惯性权重
    w_init = [Wmax-(Wmax-Wmin)*tn/tm for tn in t]

    # 绘制曲线
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 35
    plt.plot(t, w_init, color='blue', label='线性惯性权重', linewidth=5)


    # 添加标题和标签
    plt.xlabel('迭代次数', fontname='SimSun', size=35)
    plt.ylabel('数值', fontname='SimSun', size=35)
    plt.xticks(np.arange(0, Tmax + 1, 1), fontname='Times New Roman')
    plt.yticks(np.arange(0.3, Wmax + 0.1, 0.1), fontname='Times New Roman')
    plt.tick_params(labelsize=35)           # 刻度的字体大小
    plt.tick_params(direction='in')         # 指定刻度线的方向
    plt.legend(loc='upper right')


    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)

    # 显示图形
    plt.show()


if __name__ == "__main__":
    WLine(1.2, 0.3, 20)