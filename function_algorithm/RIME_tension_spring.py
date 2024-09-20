# 雾凇优化算法求解拉压弹簧问题
import random
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
random.seed(79)  # 3 12 19 72 75 79

class RIME:

    def __init__(self, restraint, dimension, Pop_size, total_iteration_num):
        self.restraint = restraint  # 边界信息
        self.dimension = dimension  # 问题维度
        self.Pop_size = Pop_size    # 种群大小
        self.total_iteration_num = total_iteration_num  # 迭代次数

    # 初始化种群
    def initialize_population(self):
        position_set = []
        for _ in range(self.Pop_size):
            position = [random.uniform(self.restraint[_][0], self.restraint[_][1]) for _ in range(len(self.restraint))]
            position_set.append(position)
        return position_set

    # 群体适应度函数
    def fitness_list_function(self, position_set):
        fitness_list = []
        for idx, position_message in enumerate(position_set):
            # 约束函数
            x1 = position_message[0]
            x2 = position_message[1]
            x3 = position_message[2]
            g1x = 1 - (x2**3*x3)/(71785*x1**4)
            g2x = (4*x2**2-x1*x2)/(12566*(x2*x1**3-x1**4)) + 1/(5108*x1**2) - 1
            g3x = 1 - (140.45*x1)/(x2**2*x3)
            g4x = (x1+x2)/1.5 - 1
            if g1x <= 0 and g2x <= 0 and g3x <= 0 and g4x <= 0:
                fitness_value = (x3+2)*x2*x1**2
            else:
                while g1x > 0 or g2x > 0 or g3x > 0 or g4x > 0:
                    x1 = random.uniform(self.restraint[0][0], self.restraint[0][1])
                    x2 = random.uniform(self.restraint[1][0], self.restraint[1][1])
                    x3 = random.uniform(self.restraint[2][0], self.restraint[2][1])
                    g1x = 1 - (x2 ** 3 * x3) / (71785 * x1 ** 4)
                    g2x = (4 * x2 ** 2 - x1 * x2) / (12566 * (x2 * x1 ** 3 - x1 ** 4)) + 1 / (5108 * x1 ** 2) - 1
                    g3x = 1 - (140.45 * x1) / (x2 ** 2 * x3)
                    g4x = (x1 + x2) / 1.5 - 1
                fitness_value = (x3+2)*x2*x1**2
                position_set[idx] = copy.deepcopy([x1, x2, x3])
            fitness_list.append(fitness_value)
        return fitness_list, position_set

    # 种群更新
    def update_position(self, now_iteration_num, best_position, position_set, fitness_list):
        theta = math.pi * now_iteration_num/(10*self.total_iteration_num)  # 参数θ
        omega = 10   # 参数w
        beta = 1 - round(omega*now_iteration_num/self.total_iteration_num)/omega
        E = math.sqrt(now_iteration_num/self.total_iteration_num)  # 附着系数E
        new_position_set = copy.deepcopy(position_set)
        # 软雾凇搜索策略
        if random.random() < E:
            new_position_set = [[0 for __ in range(self.dimension)] for _ in range(self.Pop_size)]
            for _ in range(self.Pop_size):
                for __ in range(self.dimension):
                    new_position = best_position[__] + random.uniform(-1, 1) * math.cos(theta) * beta * \
                                   (random.random() * (self.restraint[__][1] - self.restraint[__][0]) + self.restraint[__][0])
                    if new_position > self.restraint[__][1] or new_position < self.restraint[__][0]:
                        new_position = random.uniform(self.restraint[__][0], self.restraint[__][1])
                    new_position_set[_][__] = new_position

        # 硬雾凇穿刺机制
        min_fitness, max_fitness = min(fitness_list), max(fitness_list)
        # 对适应度进行归一化操作
        if min_fitness == max_fitness:
            normalized_Fitness_list = [0.5 for _ in range(len(fitness_list))]
        else:
            normalized_Fitness_list = [(fitness_list[_]-min_fitness)/(max_fitness-min_fitness) for _ in range(len(fitness_list))]
        for _ in range(self.Pop_size):
            if random.uniform(-1, 1) < normalized_Fitness_list[_]:
                new_position_set[_] = best_position
                fitness_list[_] = min_fitness

        # 正贪婪选择机制
        new_fitness_list, new_position_set = self.fitness_list_function(new_position_set)
        for _ in range(self.Pop_size):
            if new_fitness_list[_] < fitness_list[_]:
                position_set[_] = copy.copy(new_position_set[_])

        fitness_list, position_set = self.fitness_list_function(position_set)
        best_position = position_set[fitness_list.index(min(fitness_list))]
        return best_position, position_set, fitness_list

    def main(self):
        position_set = self.initialize_population()
        fitness_list, position_set = self.fitness_list_function(position_set)
        best_position = position_set[fitness_list.index(min(fitness_list))]
        best_iteration_fitness = [min(fitness_list)]
        for now_iteration_num in range(1, self.total_iteration_num+1):
            print(f"第{now_iteration_num}次迭代中")
            best_position, position_set, fitness_list = self.update_position(now_iteration_num, best_position, position_set, fitness_list)
            best_iteration_fitness.append(min(fitness_list))
        best_fitness = min(fitness_list)
        return best_position, best_fitness, fitness_list, best_iteration_fitness


if __name__ == "__main__":
    dimension = 3
    Pop_size = 100
    total_iteration_num = 100
    restraint = [[0.05, 2], [0.25, 1.3], [2, 15]]
    RIME = RIME(restraint, dimension, Pop_size, total_iteration_num)
    best_position, best_fitness, fitness_list, best_iteration_fitness = RIME.main()
    print(f"最优解坐标为{best_position} \n最优解为{best_fitness}")

    # 历次迭代的适应度曲线
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 40
    iteration_num_list = [_ for _ in range(len(best_iteration_fitness))]
    plt.plot(iteration_num_list, best_iteration_fitness, color='blue', linewidth=4)
    plt.xlabel("迭代次数", size=40)
    plt.ylabel("适应度值", size=40)
    plt.xticks(np.arange(0, len(best_iteration_fitness), 10))
    plt.scatter(total_iteration_num, min(best_iteration_fitness), color='red', marker='o', s=400)
    plt.text(total_iteration_num-25, min(best_iteration_fitness)+0.00003,
             f"f(x)={min(best_iteration_fitness):.5f}", ha='left', va='bottom')
    plt.grid()
    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)
    plt.show()