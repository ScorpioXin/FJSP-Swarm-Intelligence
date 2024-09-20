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
    # w_init = [(Wmax - Wmin) * (tm - tn)/tm + Wmin for tn in t]

    # 线性微分递减惯性权重
    w_der = [Wmax - (Wmax - Wmin)/tm**2 * tn**2 for tn in t]

    # 先增后减惯性权重
    w_in_decrease = []
    w_increase = [Wmin + 2*tn*(Wmax-Wmin)/tm for tn in t if tn/tm >= 0 and tn/tm <= 0.5]
    w_decrease = [-2*(Wmax - Wmin)*(tn/tm - 1) + Wmin for tn in t if tn/tm > 0.5 and tn/tm <= 1]
    w_in_decrease.extend(w_increase)
    w_in_decrease.extend(w_decrease)

    # 基于tansig函数的惯性权重
    w_tansig = [Wmax - (Wmax - Wmin) * (2/(1+math.exp((-8*tn)/tm))-1)**8 for tn in t]      # 要的就是这种效果


    # 绘制曲线
    linewidth = 5
    plt.plot(t, w_init, color='red', label='线性', linewidth=linewidth)
    plt.plot(t, w_der, color='green', label='线性微分递减', linewidth=linewidth)
    plt.plot(t, w_in_decrease, color='blue', label='先增后减', linewidth=linewidth)
    plt.plot(t, w_tansig, color='purple', label='基于tansig函数', linewidth=linewidth)

    # 设置全局字体及大小
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 35

    # 添加标题和标签
    # plt.title('惯性权重W变换曲线')
    plt.xlabel('迭代次数', size=35)
    plt.ylabel('数值', size=35)
    plt.xticks(np.arange(0, Tmax + 1, 1))
    plt.yticks(np.arange(0.2, Wmax + 0.2, 0.1))
    plt.tick_params(labelsize=35)           # 刻度标签的字体大小
    plt.tick_params(direction='in')         # 指定刻度线的方向
    plt.legend(loc='upper right')
    plt.grid(True)

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