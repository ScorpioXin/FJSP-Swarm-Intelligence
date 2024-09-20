# 牛顿法求解最小值
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

def f(x):
    return 3 * x ** 2 + 5

def df(x):
    return 6 * x

if __name__=='__main__':
    x = np.arange(-9, 9, 0.1)
    y = f(x)
    x0 = 7
    xt = []

# 牛顿法迭代
    for i in range(6):
        x0 = x0 - f(x0) / df(x0)
        xt.append(x0)
    xt = np.array(xt)
    print(xt)

    x_symbols = ['-10', '-8', '-6', '-4', '-2', '0', '2', '4', '6', '8', '10']
    plt.xlabel('x', fontname='Times New Roman', size=60)
    plt.ylabel('f(x)', fontname='Times New Roman', size=60)
    plt.xticks(np.arange(-10, 11, 2), x_symbols, fontname='Times New Roman')
    plt.yticks(np.arange(0, 300, 50), fontname='Times New Roman')
    # plt.yticks(np.arange(0, 300, 50), fontweight='bold')
    plt.tick_params(labelsize=35, direction='in')
    plt.plot(x, y, linewidth=5)
    plt.scatter(7, f(7), color='red', marker='o', s=400)
    plt.scatter(xt, f(xt), color='blue', marker='o', s=400)
    for i, txt in enumerate(xt):
        plt.text(txt, f(txt), str(i+1), ha='center', va='bottom', fontsize=35, fontweight='bold')
    plt.text(7, f(7), 'initial solution', fontname='Times New Roman', ha='right', va='bottom', fontsize=43, fontweight='bold')

    ax = plt.gca()
    ax.spines['top'].set_linewidth(2)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)

    plt.show()
