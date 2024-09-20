# 粒子群算法求解拉压弹簧问题
import random
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
random.seed(5)  # 3,5

class PSO:

    def __init__(self, restraint, dimension, Vmax, Vmin, Pop_size, iteration_num,
                 inertia_weight, cognitive_weight, social_weight):
        self.restraint = restraint
        self.dimension = dimension
        self.Vmax = Vmax
        self.Vmin = Vmin
        self.Pop_size = Pop_size
        self.iteration_num = iteration_num
        self.w = inertia_weight
        self.c1 = cognitive_weight
        self.c2 = social_weight

    # 初始化粒子速度和位置
    def initialize_population(self):
        velocity_set = []
        position_set = []
        for _ in range(self.Pop_size):
            velocity = [random.uniform(self.Vmin, self.Vmax) for _ in range(len(self.restraint))]
            position = [random.uniform(self.restraint[_][0], self.restraint[_][1]) for _ in range(len(self.restraint))]
            velocity_set.append(velocity)
            position_set.append(position)
        return velocity_set, position_set

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
        return fitness_list

    # 更新粒子
    def update_position(self, personal_best_position, global_best_position):
        velocity_set, position_set = self.initialize_population()
        for _ in range(self.Pop_size):
            for __ in range(self.dimension):
                new_velocity = \
                    velocity_set[_][__] + self.c1 * random.random() * (
                                personal_best_position[_][__] - position_set[_][__]) \
                    + self.c2 * random.random() * (global_best_position[__] - position_set[_][__])

                if new_velocity > self.Vmax or new_velocity < self.Vmin:  # 越界后再随机生成
                    new_velocity = random.uniform(self.Vmin, self.Vmax)
                velocity_set[_][__] = new_velocity

                # if new_velocity > self.Vmax:    # 越界后设为边界值
                #     new_velocity = self.Vmax
                # if new_velocity < self.Vmin:
                #     new_velocity = self.Vmin
                # velocity_set[_][__] = new_velocity

                new_position = position_set[_][__] + new_velocity    # 越界后再随机生成
                if new_position < self.restraint[__][0] or new_position > self.restraint[__][1]:
                    new_position = random.uniform(self.restraint[__][0], self.restraint[__][1])
                position_set[_][__] = new_position

                # new_position = position_set[_][__] + new_velocity     # 越界后设为边界值
                # if new_position > self.restraint[__][1]:
                #     new_position = self.restraint[__][1]
                # if new_position < self.restraint[__][0]:
                #     new_position = self.restraint[__][0]
                # position_set[_][__] = new_position

        return velocity_set, position_set


    def main(self):
        velocity_set, position_set = self.initialize_population()
        fitness_list = self.fitness_list_function(position_set)
        personal_best_position = position_set
        global_best_position = position_set[fitness_list.index(min(fitness_list))]
        best_iteration_fitness = [min(fitness_list)]
        for iteration in range(self.iteration_num):
            print(f"第{iteration+1}次迭代中")
            velocity_set, position_set = self.update_position(personal_best_position, global_best_position)
            new_fitness_list = self.fitness_list_function(position_set)
            for _ in range(self.Pop_size):
                if fitness_list[_] > new_fitness_list[_]:
                    fitness_list[_] = new_fitness_list[_]
                    personal_best_position[_] = position_set[_]
            global_best_position = personal_best_position[fitness_list.index(min(fitness_list))]
            best_iteration_fitness.append(min(fitness_list))
        return global_best_position, best_iteration_fitness


if __name__ == "__main__":
    restraint = [[0.05, 2], [0.25, 1.3], [2, 15]]
    dimension = 3
    Vmax = 2
    Vmin = -2
    Pop_size = 100
    iteration_num = 100
    inertia_weight = 0.8
    cognitive_weight = 1.2
    social_weight = 1.6
    PSO = PSO(restraint, dimension, Vmax, Vmin, Pop_size, iteration_num, inertia_weight, cognitive_weight, social_weight)
    global_best_position, best_iteration_fitness = PSO.main()
    print(f"最优解参数为{global_best_position} \n最优解为{min(best_iteration_fitness)}")

    # 历次迭代适应度曲线
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 45
    iteration_num_list = [_ for _ in range(len(best_iteration_fitness))]
    plt.plot(iteration_num_list, best_iteration_fitness, color='blue', linewidth=4)
    plt.xlabel("迭代次数", size=45)
    plt.ylabel("适应度值", size=45)
    plt.xticks(np.arange(0, len(best_iteration_fitness), 10))
    plt.scatter(iteration_num, min(best_iteration_fitness), color='red', marker='o', s=400)
    plt.text(iteration_num-25, min(best_iteration_fitness)+0.0001,
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