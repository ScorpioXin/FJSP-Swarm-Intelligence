# 模拟退火算法求解拉压弹簧问题
import random
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
random.seed(4)

class PSO:

    def __init__(self, restraint, dimension, Ts, Te, beta, markov):
        self.restraint = restraint
        self.dimension = dimension
        self.Ts = Ts
        self.Te = Te
        self.beta = beta
        self.markov = markov

    def generate_random_solution(self):
        x = [random.uniform(self.restraint[_][0], self.restraint[_][1]) for _ in range(len(self.restraint))]
        return x

    def generate_neighbor_solution(self, x, step_size):
        x = [x[_] + random.uniform(-step_size, step_size) for _ in range(len(x))]
        return x

    # 适应度函数
    def fitness_list_function(self, x):
        # 约束函数
        x1, x2, x3 = x[0], x[1], x[2]
        g1x = 1 - (x2 ** 3 * x3) / (71785 * x1 ** 4)
        g2x = (4 * x2 ** 2 - x1 * x2) / (12566 * (x2 * x1 ** 3 - x1 ** 4)) + 1 / (5108 * x1 ** 2) - 1
        g3x = 1 - (140.45 * x1) / (x2 ** 2 * x3)
        g4x = (x1 + x2) / 1.5 - 1
        if g1x <= 0 and g2x <= 0 and g3x <= 0 and g4x <= 0:
            fitness_value = (x3 + 2) * x2 * x1 ** 2
        else:
            while g1x > 0 or g2x > 0 or g3x > 0 or g4x > 0:
                x1 = random.uniform(self.restraint[0][0], self.restraint[0][1])
                x2 = random.uniform(self.restraint[1][0], self.restraint[1][1])
                x3 = random.uniform(self.restraint[2][0], self.restraint[2][1])
                g1x = 1 - (x2 ** 3 * x3) / (71785 * x1 ** 4)
                g2x = (4 * x2 ** 2 - x1 * x2) / (12566 * (x2 * x1 ** 3 - x1 ** 4)) + 1 / (5108 * x1 ** 2) - 1
                g3x = 1 - (140.45 * x1) / (x2 ** 2 * x3)
                g4x = (x1 + x2) / 1.5 - 1
            fitness_value = (x3 + 2) * x2 * x1 ** 2
        new_x = copy.deepcopy([x1, x2, x3])
        return fitness_value, new_x

    def upgrade_solution(self, temperature, fitness, x, best_x):
        new_x = self.generate_random_solution()
        new_fitness, new_x = self.fitness_list_function(new_x)
        if new_fitness < fitness:                   # 保留最优解
            best_x = new_x
        # 若候选解为较劣解，以一定的概率接受它。但是对于这个问题而言，当前解和候选解的适应度数值差距太大，所以导致接受候选解的概率极低，
        # 将温度调到很高的时候可以发现是可以接受较劣解的。
        if new_fitness < fitness or random.random() < math.exp(-(new_fitness - fitness)/temperature):
            x = copy.deepcopy(new_x)
            fitness = new_fitness
        return x, fitness, best_x

    def main(self):
        x = self.generate_random_solution()
        fitness, x = self.fitness_list_function(x)
        best_x = copy.deepcopy(x)

        temperature = self.Ts
        iteration_fitness = []
        while temperature >= self.Te:       # 基本模拟退火
            print(f"首次降火中，温度为{temperature}")
            iteration_fitness.append(fitness)
            for _ in range(self.markov):
                x, fitness, best_x = self.upgrade_solution(temperature, fitness, x,  best_x)
            temperature *= self.beta

        temperature = self.Ts
        best_iteration_fitness = []
        while temperature >= self.Te:       # 在最优解的邻域中再次退火(只接受较优解)
            print(f"再次降火中，温度为{temperature}")
            now_best_fitness, x = self.fitness_list_function(best_x)
            best_iteration_fitness.append(now_best_fitness)
            for _ in range(self.markov):
                new_x = self.generate_neighbor_solution(best_x, 0.5)
                new_fitness, new_x = self.fitness_list_function(new_x)
                if new_fitness < now_best_fitness:
                    best_x = new_x
            temperature *= self.beta

        return best_x, fitness, iteration_fitness, best_iteration_fitness

if __name__ == "__main__":
    restraint = [[0.05, 2], [0.25, 1.3], [2, 15]]
    dimension = 3
    Ts = 300
    Te = 1
    beta = 0.99
    markov = 20
    PSO = PSO(restraint, dimension, Ts, Te, beta, markov)
    best_x, fitness, iteration_fitness, best_iteration_fitness = PSO.main()
    print(f"最优解参数为{best_x} \n最优解为{min(best_iteration_fitness)}")

   # 历次迭代的适应度曲线
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['font.size'] = 40
    iteration_num_list = [_ for _ in range(len(iteration_fitness))]
    plt.plot(iteration_num_list, iteration_fitness, color='blue', linewidth=3)
    # plt.title("首次退火的适应度曲线")
    plt.xlabel("迭代次数", size=40)
    plt.ylabel("适应度值", size=40)
    plt.xticks(np.arange(0, len(iteration_fitness), 50))
    plt.scatter(iteration_fitness.index(min(iteration_fitness)), min(iteration_fitness), color='red', marker='o', s=400)
    plt.text(iteration_fitness.index(min(iteration_fitness))+10, min(iteration_fitness)-0.015,
             f"f(x)={round(best_iteration_fitness[0], 5)}", ha='left', va='bottom')

    plt.scatter(len(iteration_fitness)-1, iteration_fitness[-1], color='blue', marker='o', s=400)
    plt.text(len(iteration_fitness)-80, iteration_fitness[-1]+0.003, f"f(x)={round(fitness, 5)}", ha='left', va='bottom')
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
    plt.rcParams['font.size'] = 40
    iteration_num_list = [_ for _ in range(len(best_iteration_fitness))]
    plt.plot(iteration_num_list, best_iteration_fitness, color='blue', linewidth=3)
    # plt.title("再次退火适应度曲线")
    plt.xlabel("迭代次数", size=40)
    plt.ylabel("适应度值", size=40)
    plt.xticks(np.arange(0, len(best_iteration_fitness), 50))
    plt.scatter(0, max(best_iteration_fitness), color='red', marker='o', s=400)
    plt.text(10, max(best_iteration_fitness)-0.0007, f"f(x)={round(best_iteration_fitness[0], 5)}", ha='left', va='bottom')

    plt.scatter(len(best_iteration_fitness)-1, min(best_iteration_fitness), color='green', marker='o', s=400)
    plt.text(len(iteration_fitness)-150, min(best_iteration_fitness),
             f"f(x)={min(best_iteration_fitness):.5f}", ha='left', va='bottom')
    plt.grid()
    ax = plt.gca()
    width = 2
    ax.spines['top'].set_linewidth(width)  # 设置顶部边框线的宽度为2
    ax.spines['bottom'].set_linewidth(width)
    ax.spines['left'].set_linewidth(width)
    ax.spines['right'].set_linewidth(width)
    plt.show()