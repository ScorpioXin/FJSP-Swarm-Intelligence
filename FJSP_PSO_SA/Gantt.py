from Pro_Data import Pro_Data

import threading
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
'''matplotlib 的 backend的默认渲染器是agg，
agg是一个没有图形显示界面的终端，如果要图像正常显示，
则需要切换为图形界面显示的终端TkAgg'''

# 画甘特图
def Gantt(plt_item, fitness):
    """
    :param plt_item: 需要进行绘图的数据表(最佳调度方案的信息列表)
    :param fitness:  完工时间
    """
    pro_m, pro_t, J_num, machine_num = Pro_Data()
    color_set = ['red', 'Aqua', 'yellow', 'orange', 'green', 'mediumslateblue', 'purple', 'pink', 'navajowhite', 'Thistle',
         'Magenta', 'SlateBlue', 'RoyalBlue', 'blue', 'floralwhite', 'ghostwhite', 'goldenrod', 'moccasin',
         'navajowhite', 'navy', 'sandybrown']

    # 设置全局字体及大小
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 35

    # Optimal_dispatch_scheme = [[10, 1, 6.0, 0, 2.0], [1, 1, 1.0, 0, 5.0], [7, 1, 6.0, 2.0, 3.0],·····
    for i in range(len(plt_item)):
        Job_id = plt_item[i][0]
        Job_flow = plt_item[i][1]
        Machine_id = int(plt_item[i][2])
        Start_time = plt_item[i][3]
        End_time = plt_item[i][4]
        plt.barh(Machine_id, width=End_time - Start_time, height=0.8, left=Start_time,
                 color=color_set[Job_id - 1], edgecolor='black')
        plt.text(x=Start_time + ((End_time - Start_time) / 2 - 0.5), y=Machine_id - 0.05,   # 在图表中添加文本注释(x,y,s,size,fontproperties):(X轴位置,Y轴位置,字符串标签,大小,字体)
                 s=str(f'{Job_id},{Job_flow}'), rotation=90, size=25, fontproperties='Times New Roman')

    plt.yticks(np.arange(1, machine_num + 1), np.arange(1, machine_num + 1), fontproperties='Times New Roman')    # 设置y轴刻度标签：(y轴刻度的位置,y轴刻度标签的文本内容)
    plt.ylabel("机器", fontproperties='SimSun')
    plt.xlabel("时间", fontproperties='SimSun')
    plt.title(f"{J_num}个工件，{machine_num}台机器的调度甘特图----完工时间：{fitness}", fontproperties='SimSun')
    plt.tick_params(labelsize=35)           # 刻度标签的字体大小
    plt.tick_params(direction='in')         # 指定刻度线的方向
    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)
    plt.show()

# 画折线图
def Line_Chart(fitness_iter_list, iteration_num):
    iteration_num_list = [_ for _ in range(0, iteration_num+1)]
    plt.plot(iteration_num_list, fitness_iter_list, color='blue', linewidth=4)
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 35
    plt.title("历次迭代后最优加工时间", fontproperties='SimSun')
    plt.xlabel("迭代次数", size=35, fontproperties='SimSun')
    plt.ylabel("加工时间", size=35, fontproperties='SimSun')
    plt.tick_params(labelsize=35)           # 刻度标签的字体大小
    plt.tick_params(direction='in')         # 指定刻度线的方向
    plt.xticks(range(int(min(iteration_num_list)), int(max(iteration_num_list)) + 1, 2))
    plt.yticks(range(int(min(fitness_iter_list)), int(max(fitness_iter_list)) + 1, 2))
    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)
    plt.show()

if __name__ == "__main__":
    plt_item = [[10, 1, 6.0, 0, 2.0], [1, 1, 1.0, 0, 5.0], [7, 1, 6.0, 2.0, 3.0]]
    fitness = 5
    Gantt(plt_item, fitness)

    fitness_iter_list = [60, 59, 57, 55, 50]
    iteration_num = 5
    Line_Chart(fitness_iter_list, iteration_num)