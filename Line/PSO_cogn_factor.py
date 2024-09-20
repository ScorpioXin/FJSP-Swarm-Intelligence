import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

# 作惯性权重的曲线图
def WLine(C1s, C1e, C2s, C2e, Tmax):

    t = np.arange(0, Tmax+0.1, 0.1)
    tm = max(t)
    C1_linear = [C1s + (C1e - C1s)*tn/tm for tn in t]
    C2_linear = [C2s + (C2e - C2s)*tn/tm for tn in t]
    C1_non_linear = [C1s + (C1e - C1s)*(1 - (np.arccos(-2*tn/tm + 1))/np.pi) for tn in t]
    C2_non_linear = [C2s + (C2e - C2s)*(1 - (np.arccos(-2*tn/tm + 1))/np.pi) for tn in t]

    # 绘制曲线
    linewidth = 5
    plt.plot(t, C1_linear, color='red', label='线性认知因子C1', linewidth=linewidth)
    plt.plot(t, C2_linear, color='green', label='线性认知因子C2', linewidth=linewidth)
    plt.plot(t, C1_non_linear, color='blue', label='非线性认知因子C1', linewidth=linewidth)
    plt.plot(t, C2_non_linear, color='purple', label='非线性认知因子C2', linewidth=linewidth)

    # 设置全局字体及大小
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 35

    # 添加标题和标签
    plt.xlabel('迭代次数', size=35)
    plt.ylabel('数值', size=35)
    plt.xticks(np.arange(0, Tmax + 1, 1))
    plt.yticks(np.arange(0.2, max(C1s, C1e, C2s, C2e) + 0.2, 0.1))
    plt.tick_params(labelsize=35)           # 刻度标签的字体大小
    plt.tick_params(direction='in')         # 指定刻度线的方向
    plt.legend(loc='upper center')
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
    WLine(1.2, 0.3, 0.3, 1.2, 20)