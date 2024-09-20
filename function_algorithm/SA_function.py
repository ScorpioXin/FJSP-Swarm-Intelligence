# 模拟退火算法求解最小值
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
random.seed(3)

class SA:
    def __init__(self, Ts, Te, beta, markov):
        self.Ts = Ts
        self.Te = Te
        self.beta = beta
        self.markov = markov

    def generate_random_solution(self):
        new_x = random.uniform(-10, 10)
        new_y = random.uniform(-10, 10)
        return new_x, new_y

    def generate_neighbor_solution(self, x, y, step_size):
        new_x = x + random.uniform(-step_size, step_size)
        new_y = y + random.uniform(-step_size, step_size)
        return new_x, new_y

    def fitness_function(self, x, y):
        fitness = x**2 + y**2 - abs(1.5 * x * y)
        return fitness

    def upgrade_solution(self, temperature, coordinate, fitness, best_x, best_y):
        new_x, new_y = self.generate_random_solution()
        new_fitness = self.fitness_function(new_x, new_y)
        if new_fitness < fitness:                   # 保留最优解
            best_x, best_y = new_x, new_y
        if new_fitness < fitness or random.random() < math.exp(-(new_fitness - fitness)/temperature):
            coordinate[0], coordinate[1] = new_x, new_y
            fitness = new_fitness
        return coordinate, fitness, best_x, best_y

    def main(self):
        best_x, best_y = self.generate_random_solution()
        coordinate = [best_x, best_y]
        fitness = self.fitness_function(best_x, best_y)

        temperature = self.Ts
        iteration_fitness = []
        # iteration_temperature = []
        while temperature >= self.Te:       # 基本模拟退火
            iteration_fitness.append(fitness)
            # iteration_temperature.append(temperature)
            for _ in range(self.markov):
                coordinate, fitness, best_x, best_y = \
                    self.upgrade_solution(temperature, coordinate, fitness, best_x, best_y)
            temperature *= self.beta

        temperature = self.Ts
        best_iteration_fitness = []
        while temperature >= self.Te:       # 在最优解的邻域中再次退火(只接受较优解)
            now_best_fitness = self.fitness_function(best_x, best_y)
            best_iteration_fitness.append(now_best_fitness)
            for _ in range(self.markov):
                new_x, new_y = self.generate_neighbor_solution(best_x, best_y, 0.5)
                if self.fitness_function(new_x, new_y) < now_best_fitness:
                    best_x, best_y = new_x, new_y
            temperature *= self.beta

        return coordinate, fitness, iteration_fitness, best_x, best_y, best_iteration_fitness

if __name__ == "__main__":
    Ts = 300
    Te = 1
    beta = 0.98
    markov = 20
    SA = SA(Ts, Te, beta, markov)
    coordinate, fitness, iteration_fitness, best_x, best_y, best_iteration_fitness = SA.main()

    best_coordinate = [best_x, best_y]
    best_fitness = best_x**2 + best_y**2 - abs(1.5 * best_x * best_y)
    print(f"首次退火最终坐标：{coordinate}")
    print(f"首次退火最终适应度：{fitness}")
    print(f"再次退火最优坐标：{best_coordinate}")
    print(f"再次退火最优适应度：{best_fitness:.8f}")

    # 历次迭代的适应度曲线
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 40
    iteration_num_list = [_ for _ in range(len(iteration_fitness))]
    plt.plot(iteration_num_list, iteration_fitness, color='blue', linewidth=3)
    plt.xlabel("迭代次数", size=40)
    plt.ylabel("适应度值", size=40)
    plt.xticks(np.arange(0, len(iteration_fitness), 50))
    plt.yticks(np.arange(0, max(iteration_fitness)+10, 10))
    plt.scatter(iteration_fitness.index(min(iteration_fitness)), min(iteration_fitness),
                color='red', marker='o', s=400)
    # plt.text(iteration_fitness.index(min(iteration_fitness))-50, min(iteration_fitness)-4,
    #          f"f(x,y)={round(best_iteration_fitness[0], 7)}", ha='left', va='bottom')
    # plt.text(iteration_fitness.index(min(iteration_fitness))-5, min(iteration_fitness)-0.8,
    #          f"f(x,y)={round(best_iteration_fitness[0], 7)}", ha='left', va='bottom')

    plt.scatter(len(iteration_fitness)-1, fitness, color='blue', marker='o', s=400)
    # plt.text(len(iteration_fitness)-20, fitness+1,
    #          f"f(x,y)={round(fitness, 7)}", ha='left', va='bottom')
    # plt.text(len(iteration_fitness)-10, fitness+0.3, f"f(x,y)={round(fitness, 7)}", ha='left', va='bottom')
    plt.grid()
    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)
    plt.show()

    # 保留最优解，再次退火迭代的适应度曲线
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 43
    iteration_num_list = [_ for _ in range(len(best_iteration_fitness))]
    plt.plot(iteration_num_list, best_iteration_fitness, color='blue', linewidth=3)
    plt.xlabel("迭代次数", size=43)
    plt.ylabel("适应度值", size=43)
    plt.xticks(np.arange(0, len(best_iteration_fitness), 40))
    plt.yticks(np.arange(0, max(best_iteration_fitness)+0.002, 0.002))
    plt.scatter(0, max(best_iteration_fitness), color='red', marker='o', s=400)
    plt.text(2, max(best_iteration_fitness)-0.0008,
             f"f(x,y)={round(min(iteration_fitness), 7)}", ha='left', va='bottom')
    plt.scatter(best_iteration_fitness.index(min(best_iteration_fitness)), min(best_iteration_fitness),
                color='green', marker='o', s=400)
    plt.text(best_iteration_fitness.index(min(best_iteration_fitness)), min(best_iteration_fitness)+0.000008,
             f"f(x,y)={min(best_iteration_fitness):.7f}", ha='left', va='bottom')
    plt.grid()

    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)

    plt.show()