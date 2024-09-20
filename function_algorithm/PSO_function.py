# 粒子群算法求解函数最小值
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
random.seed(24)

class PSO:

    def __init__(self, Pmax, Pmin, Vmax, Vmin, dimension, Pop_size, iteration_num,
                 inertia_weight, cognitive_weight, social_weight):
        self.Pmax = Pmax
        self.Pmin = Pmin
        self.Vmax = Vmax
        self.Vmin = Vmin
        self.dimension = dimension
        self.Pop_size = Pop_size
        self.iteration_num = iteration_num
        self.w = inertia_weight
        self.c1 = cognitive_weight
        self.c2 = social_weight

    # 初始化粒子速度和位置
    def initialize_particle(self):
        velocity_set = []
        position_set = []
        for _ in range(self.Pop_size):
            velocity = [random.uniform(self.Vmin, self.Vmax), random.uniform(self.Vmin, self.Vmax)]
            position = [random.uniform(self.Pmin, self.Pmax), random.uniform(self.Pmin, self.Pmax)]
            velocity_set.append(velocity)
            position_set.append(position)
        return velocity_set, position_set

    # 适应度函数
    def fitness_function(self, position_set):
        fitness_list = []
        for position_message in position_set:
            fitness_value = position_message[0]**2 + position_message[1]**2 - \
                            abs(1.5*position_message[0]*position_message[1])
            fitness_list.append(fitness_value)
        return fitness_list

    # 更新粒子
    def update_particle(self, personal_best_position, global_best_position):
        velocity_set, position_set = self.initialize_particle()
        for _ in range(self.Pop_size):
            for __ in range(self.dimension):
                new_velocity = \
                    velocity_set[_][__] + self.c1*random.random()*(personal_best_position[_][__]-position_set[_][__]) \
                    + self.c2*random.random()*(global_best_position[__]-position_set[_][__])

                if new_velocity > self.Vmax or new_velocity < self.Vmin:    # 越界后再随机生成
                    new_velocity = random.uniform(self.Vmin, self.Vmax)
                velocity_set[_][__] = new_velocity

                new_position = position_set[_][__] + new_velocity
                if new_position > self.Pmax or new_position < self.Pmin:
                    new_position = random.uniform(self.Pmin, self.Pmax)
                position_set[_][__] = new_position

                # if new_velocity > self.Vmax:    # 越界后设为边界值
                #     new_velocity = self.Vmax
                # if new_velocity < self.Vmin:
                #     new_velocity = self.Vmin
                # velocity_set[_][__] = new_velocity
                #
                # new_position = position_set[_][__] + new_velocity
                # if new_position > self.Pmax:
                #     new_position = self.Pmax
                # if new_position < self.Pmin:
                #     new_position = self.Pmin
                # position_set[_][__] = new_position

        return velocity_set, position_set

    def main(self):
        velocity_set, position_set = self.initialize_particle()
        fitness_list = self.fitness_function(position_set)
        personal_best_position = position_set
        global_best_position = position_set[fitness_list.index(min(fitness_list))]
        iteration_best_fitness = [min(fitness_list)]
        middle_position_set = []
        for iteration in range(self.iteration_num):
            velocity_set, position_set = self.update_particle(personal_best_position, global_best_position)
            new_fitness_list = self.fitness_function(position_set)
            for _ in range(self.Pop_size):
                if fitness_list[_] > new_fitness_list[_]:
                    fitness_list[_] = new_fitness_list[_]
                    personal_best_position[_] = position_set[_]
            global_best_position = personal_best_position[fitness_list.index(min(fitness_list))]
            iteration_best_fitness.append(min(fitness_list))
            # if 98 <= iteration and iteration <= 100:
            #     middle_position_set.append(position_set)
        return global_best_position, iteration_best_fitness

if __name__ == "__main__":
    Pmax = 10
    Pmin = -10
    Vmax = 3
    Vmin = -3
    dimension = 2
    Pop_size = 30
    iteration_num = 100
    inertia_weight = 0.8
    cognitive_weight = 0.6
    social_weight = 0.4
    pso = PSO(Pmax, Pmin, Vmax, Vmin, dimension, Pop_size, iteration_num,
              inertia_weight, cognitive_weight, social_weight)
    global_best_position, iteration_best_fitness = pso.main()
    # print(global_best_position)
    # print(min(iteration_best_fitness))

    # x_message_set = []
    # y_message_set = []
    # for _ in range(len(middle_position_set)):
    #     x_message = []
    #     y_message = []
    #     for __ in range(len(middle_position_set[_])):
    #         x_message.append(middle_position_set[_][__][0])
    #         y_message.append(middle_position_set[_][__][1])
    #     x_message_set.append(x_message)
    #     y_message_set.append(y_message)
    # for _ in range(len(x_message_set)):
    #     plt.rcParams['font.sans-serif'] = ['SimSun']
    #     plt.rcParams['font.size'] = 23
    #     plt.xlabel("x")
    #     plt.ylabel("y")
    #     plt.xticks(np.arange(-10, 10, 1))
    #     plt.yticks(np.arange(-10, 10, 1))
    #     plt.scatter(x_message_set[0], y_message_set[1], color='red', marker='o', s=100)
    #     plt.grid()
    #     plt.show()

    # 历次迭代适应度曲线
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 45
    iteration_num_list = [_ for _ in range(0, iteration_num+1)]
    plt.plot(iteration_num_list, iteration_best_fitness, color='blue', linewidth=4)
    plt.xlabel("迭代次数", size=45)
    plt.ylabel("适应度值", size=45)
    plt.xticks(np.arange(0, iteration_num + 1, 10))
    plt.yticks(np.arange(0, max(iteration_best_fitness) + 0.1, 0.2))
    plt.scatter(iteration_num, min(iteration_best_fitness), color='red', marker='o', s=400)
    plt.text(iteration_num-45, min(iteration_best_fitness)+0.02,
             f"f(x,y)={round(min(iteration_best_fitness), 8)}"
             f"\n(x,y)=({round(global_best_position[0], 5)},{round(global_best_position[1], 5)})",
             ha='left', va='bottom')
    plt.grid()

    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)

    plt.show()


