# 雾凇优化算法求解函数最小值
import random
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
random.seed(7)

class RIME:

    def __init__(self, Pmax, Pmin, dimension, Pop_size, total_iteration_num):
        self.Pmax = Pmax    # 上边界
        self.Pmin = Pmin    # 下边界
        self.dimension = dimension  # 问题维度
        self.Pop_size = Pop_size    # 种群大小
        self.total_iteration_num = total_iteration_num  # 迭代次数

    # 初始化种群
    def initialize_population(self):
        position_set = []
        for _ in range(self.Pop_size):
            position = [random.uniform(self.Pmin, self.Pmax), random.uniform(self.Pmin, self.Pmax)]
            position_set.append(position)
        return position_set

    # 群体适应度函数
    def fitness_list_function(self, position_set):
        fitness_list = []
        for position_message in position_set:
            fitness_value = position_message[0]**2 + position_message[1]**2 - abs(1.5*position_message[0]*position_message[1])
            fitness_list.append(fitness_value)
        return fitness_list

    # 种群更新
    def update_position(self, now_iteration_num, best_position, position_set, fitness_list):
        theta = math.pi * now_iteration_num/(10*self.total_iteration_num)  # 参数θ
        omega = 5   # 参数w
        beta = 1 - round(omega*now_iteration_num/self.total_iteration_num)/omega
        E = math.sqrt(now_iteration_num/self.total_iteration_num)  # 附着系数E
        new_position_set = copy.deepcopy(position_set)
        # 软雾凇搜索策略
        if random.random() < E:
            new_position_set = [[0 for __ in range(self.dimension)] for _ in range(self.Pop_size)]
            for _ in range(self.Pop_size):
                for __ in range(self.dimension):
                    new_position = best_position[__] + random.uniform(-1, 1) * math.cos(theta) * beta * \
                                   (random.random() * (self.Pmax - self.Pmin) + self.Pmin)
                    if new_position > self.Pmax or new_position < self.Pmin:
                        new_position = random.uniform(self.Pmin, self.Pmax)
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
        new_fitness_list = self.fitness_list_function(new_position_set)
        for _ in range(self.Pop_size):
            if new_fitness_list[_] < fitness_list[_]:
                position_set[_] = copy.copy(new_position_set[_])

        fitness_list = self.fitness_list_function(position_set)
        best_position = position_set[fitness_list.index(min(fitness_list))]
        return best_position, position_set, fitness_list

    def main(self):
        position_set = self.initialize_population()
        fitness_list = self.fitness_list_function(position_set)
        best_position = position_set[fitness_list.index(min(fitness_list))]
        best_iteration_fitness = [min(fitness_list)]
        for now_iteration_num in range(1, self.total_iteration_num+1):
            best_position, position_set, fitness_list = self.update_position(now_iteration_num, best_position, position_set, fitness_list)
            best_iteration_fitness.append(min(fitness_list))
        best_fitness = min(fitness_list)
        return best_position, best_fitness, fitness_list, best_iteration_fitness


if __name__ == "__main__":
    Pmax = 10
    Pmin = -10
    dimension = 2
    Pop_size = 50
    total_iteration_num = 100
    RIME = RIME(Pmax, Pmin, dimension, Pop_size, total_iteration_num)
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
    plt.yticks(np.arange(0, max(best_iteration_fitness), 0.2))
    plt.scatter(total_iteration_num, min(best_iteration_fitness), color='red', marker='o', s=400)
    plt.text(total_iteration_num-26, min(best_iteration_fitness)+0.03,
             f"x={best_position[0]:.2e}"
             f"\ny={best_position[1]:.2e}"
             f"\nf(x,y)={min(best_iteration_fitness):.2e}",
             ha='left', va='bottom')
    plt.grid()
    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)
    plt.show()