# 雾凇优化算法求解三杆桁架问题
import random
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
random.seed(36)  # 22 23 28 33 36 54 57

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
            L = 100
            P = 2
            delta = 2
            x1 = position_message[0]
            x2 = position_message[1]
            g1x = (math.sqrt(2)*x1+x2)/(math.sqrt(2)*x1**2+2*x1*x2)*P - delta
            g2x = x2/(math.sqrt(2)*x1**2+2*x1*x2)*P - delta
            g3x = 1/(math.sqrt(2)*x2+x1)*P - delta
            if g1x <= 0 and g2x <= 0 and g3x <= 0:
                fitness_value = (2*math.sqrt(2)*x1+x2) * L
            else:
                while g1x > 0 or g2x > 0 or g3x > 0:
                    x1 = random.uniform(self.restraint[0][0], self.restraint[0][1])
                    x2 = random.uniform(self.restraint[1][0], self.restraint[1][1])
                    g1x = (math.sqrt(2) * x1 + x2) / (math.sqrt(2) * x1 ** 2 + 2 * x1 * x2) * P - delta
                    g2x = x2 / (math.sqrt(2) * x1 ** 2 + 2 * x1 * x2) * P - delta
                    g3x = 1 / (math.sqrt(2) * x2 + x1) * P - delta
                fitness_value = (2*math.sqrt(2)*x1+x2) * L
                position_set[idx] = copy.deepcopy([x1, x2])
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
    restraint = [[0.001, 1], [0.001, 1]]
    dimension = 2
    Pop_size = 50
    total_iteration_num = 100
    RIME = RIME(restraint, dimension, Pop_size, total_iteration_num)
    best_position, best_fitness, fitness_list, best_iteration_fitness = RIME.main()
    print(f"最优解坐标为{best_position} \n最优解为{best_fitness}")

    # 历次迭代的适应度曲线
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 23
    iteration_num_list = [_ for _ in range(len(best_iteration_fitness))]
    plt.plot(iteration_num_list, best_iteration_fitness)
    plt.xlabel("迭代次数")
    plt.ylabel("适应度值")
    plt.xticks(np.arange(0, len(best_iteration_fitness), 10))
    plt.scatter(total_iteration_num, min(best_iteration_fitness), color='red', marker='o', s=100)
    plt.text(total_iteration_num-15, min(best_iteration_fitness)+0.1,
             f"f(x)={min(best_iteration_fitness):.5f}", ha='left', va='bottom')
    plt.grid()
    plt.show()