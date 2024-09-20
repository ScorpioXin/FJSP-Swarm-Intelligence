# 斑马优化算法求解拉压弹簧问题
import random
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
random.seed(5)

class ZOA:

    def __init__(self, restraint, dimension, Pop_size, total_iteration_num):
        self.restraint = restraint
        self.dimension = dimension
        self.Pop_size = Pop_size
        self.total_iteration_num = total_iteration_num

    # 初始化斑马群位置
    def initialize_population(self):
        position_set = []
        for _ in range(self.Pop_size):
            position = [random.uniform(self.restraint[_][0], self.restraint[_][1]) for _ in range(len(self.restraint))]
            position_set.append(position)
        return position_set

    # 群体适应度函数
    def fitness_list_function(self, position_set):
        fitness_list = []
        for position_message in position_set:
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
                fitness_value = 1e10
            fitness_list.append(fitness_value)
        return fitness_list

    # 更新斑马群位置
    def update_position(self, now_iteration_num, position_set, fitness_list):
        # 第一阶段（觅食阶段）
        best_position = position_set[fitness_list.index(min(fitness_list))]
        new_position_set = [[0 for __ in range(self.dimension)] for _ in range(self.Pop_size)]
        for _ in range(self.Pop_size):
            for __ in range(self.dimension):
                new_position = position_set[_][__] + random.uniform(0, 1) * \
                               (best_position[__] - round(1+random.random()) * best_position[__])
                if new_position < self.restraint[__][0] or new_position > self.restraint[__][1]:
                    new_position = random.uniform(self.restraint[__][0], self.restraint[__][1])
                new_position_set[_][__] = new_position
        new_fitness_list = self.fitness_list_function(new_position_set)
        for _ in range(len(new_fitness_list)):
            if new_fitness_list[_] < fitness_list[_]:
                fitness_list[_] = copy.copy(new_fitness_list[_])
                position_set[_] = copy.copy(new_position_set[_])

        # 第二阶段（防御阶段）
        Ps = random.random()
        if Ps <= 0.5:
            for _ in range(self.Pop_size):
                for __ in range(self.dimension):
                    new_position = position_set[_][__] + 0.01*(2*random.random()-1) * \
                                   (1-now_iteration_num/self.total_iteration_num) * position_set[_][__]
                    if new_position < self.restraint[__][0] or new_position > self.restraint[__][1]:
                        new_position = random.uniform(self.restraint[__][0], self.restraint[__][1])
                    new_position_set[_][__] = new_position
        else:
            attacked_position = position_set[random.randrange(0, self.Pop_size)]
            for _ in range(self.Pop_size):
                for __ in range(self.dimension):
                    new_position = position_set[_][__] + random.random() * \
                                   (attacked_position[__] - round(1+random.random()) * position_set[_][__])
                    if new_position < self.restraint[__][0] or new_position > self.restraint[__][1]:
                        new_position = random.uniform(self.restraint[__][0], self.restraint[__][1])
                    new_position_set[_][__] = new_position
        new_fitness_list = self.fitness_list_function(new_position_set)
        for _ in range(len(new_fitness_list)):
            if new_fitness_list[_] < fitness_list[_]:
                fitness_list[_] = new_fitness_list[_]
                position_set[_] = new_position_set[_]
        return position_set, fitness_list


    def main(self):
        position_set = self.initialize_population()
        fitness_list = self.fitness_list_function(position_set)
        best_iteration_fitness = [min(fitness_list)]
        for now_iteration_num in range(1, self.total_iteration_num+1):
            position_set, fitness_list = self.update_position(now_iteration_num, position_set, fitness_list)
            best_iteration_fitness.append(min(fitness_list))
        best_fitness = min(best_iteration_fitness)
        best_position = position_set[fitness_list.index(best_fitness)]
        return best_position, best_fitness, fitness_list, best_iteration_fitness


if __name__ == "__main__":
    dimension = 3
    Pop_size = 100
    total_iteration_num = 200
    restraint = [[0.05, 2], [0.25, 1.3], [2, 15]]
    ZOA = ZOA(restraint, dimension, Pop_size, total_iteration_num)
    best_position, best_fitness, fitness_list, best_iteration_fitness = ZOA.main()
    print(f"最优解参数为{best_position} \n最优解为{best_fitness}")

    # 历次迭代的适应度曲线
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 43
    iteration_num_list = [_ for _ in range(len(best_iteration_fitness))]
    plt.plot(iteration_num_list, best_iteration_fitness, color='blue', linewidth=4)
    plt.xlabel("迭代次数", size=43)
    plt.ylabel("适应度值", size=43)
    plt.xticks(np.arange(0, len(best_iteration_fitness), 50))
    plt.scatter(total_iteration_num, min(best_iteration_fitness), color='red', marker='o', s=400)
    plt.text(total_iteration_num-45, min(best_iteration_fitness)+0.0005,
             f"f(x)={min(best_iteration_fitness):.5f}",
             ha='left', va='bottom')
    plt.grid()
    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)
    plt.show()