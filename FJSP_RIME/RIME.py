from Pro_Data import Pro_Data
from Encode import Init_Pop
from Decode import Decode, Dispatch, Fitness
from Gantt import Gantt, Line_Chart

import math
import copy
import random
random.seed(521)  # 521,555,19,28

class RIME:

    def __init__(self, Pop_size, iteration_num):
        self.Pop_size = Pop_size  # 种群大小
        self.iteration_num = iteration_num  # 迭代次数

    # 将三维的加工机器信息转化为二维列表
    def machine_message(self):
        process_machine = []
        for _ in range(len(pro_m)):
            for __ in pro_m[_]:
                process_machine.append(__)
        return process_machine

    def location_scheduling_conversion(self, ms_position_set, os_position_set, process_machine):
        """
        位置与调度编码的转换函数
        :param ms_position_set: MS的位置信息集合，形式如[[1.3, 2.4, -1.5, ···], [], ···]
        :param os_position_set: OS的位置信息集合，形式如[[1.3, 2.4, -1.5, ···], [], ···]
        :param process_machine: 加工机器信息
        :return: new_MS为位置信息转换成整数编码后的MS，形式如[[2, 1, 3, ···], [], ···];
                 new_OS为位置信息转换成整数编码后的OS，形式如[[1, 2, 2, ···], [], ···]
        """
        # MS部分位置转换
        dimension = len(ms_position_set[0])
        new_MS = [[0 for __ in range(dimension)] for _ in range(self.Pop_size)]
        new_OS= [[0 for __ in range(dimension)] for _ in range(self.Pop_size)]
        for _, ms_position in enumerate(ms_position_set):
            for __ in range(len(ms_position)):
                if round(ms_position[__]) in range(1, len(process_machine[__])+1):
                    new_MS[_][__] = round(ms_position_set[_][__])
                else:
                    new_MS[_][__] = random.randint(1, len(process_machine[__]))

        # OS部分位置转换
        os = [0 for _ in range(len(process_machine))]
        copy_os_position_set = copy.deepcopy(os_position_set)
        for idx, os_position in enumerate(copy_os_position_set):
            copy_os_position = copy.deepcopy(os_position)   # 深度拷贝副本，避免直接修改os_position，因为copy_os_position_set也跟着变
            for i in range(1, J_num+1):
                for j in range(len(pro_m[i-1])):
                    min_idx = copy_os_position.index(min(copy_os_position))
                    os[min_idx] = i
                    copy_os_position[min_idx] = int(1e5)
            new_OS[idx] = os

        return new_MS, new_OS

    def update_MS_OS(self, ms_position_set, os_position_set, new_ms_position_set, new_os_position_set, new_MS, new_OS, Fitness_list, MS, OS):
        """
        判断是否更新MS和OS,候选解更优则更新,否则不更新
        :param ms_position_set: MS的位置信息集合，形式如[[1.3, 2.4, -1.5, ···], [], ···]
        :param os_position_set: OS的位置信息集合，形式如[[1.3, 2.4, -1.5, ···], [], ···]
        :param new_ms_position_set: MS的候选位置信息集合，形式如[[1.3, 2.4, -1.5, ···], [], ···]
        :param new_os_position_set: OS的候选位置信息集合，形式如[[1.3, 2.4, -1.5, ···], [], ···]
        :param new_MS: 位置信息转换成整数编码后的MS，形式如[[2, 1, 3, ···], [], ···]
        :param new_OS: 位置信息转换成整数编码后的OS，形式如[[1, 2, 2, ···], [], ···]
        :param Fitness_list: 种群的适应度列表，形式如[45, 67, 56, ···]
        :param MS: 机器选择部分编码
        :param OS: 工序排序部分编码
        :return: ms_position_set为MS更新后的位置信息集合;
                 os_position_set为OS更新后的位置信息集合;
                 Fitness_list为更新后的种群适应度列表;
                 MS为更新后的机器选择部分编码;
                 OS为更新后的工序排序部分编码
        """
        new_Pro_Message_set = Decode(new_MS, new_OS)
        new_P_dispatch_set = Dispatch(new_Pro_Message_set)
        new_Fitness_list = Fitness(new_P_dispatch_set)
        # 正贪婪选择机制
        for _ in range(len(new_Fitness_list)):
            if new_Fitness_list[_] < Fitness_list[_]:
                Fitness_list[_] = new_Fitness_list[_]
                ms_position_set[_] = copy.copy(new_ms_position_set[_])
                os_position_set[_] = copy.copy(new_os_position_set[_])
                MS[_] = copy.deepcopy(new_MS[_])
                OS[_] = copy.deepcopy(new_OS[_])
        return ms_position_set, os_position_set, Fitness_list, MS, OS

    # 种群更新
    def update_population(self, now_iteration_num, ms_position_set, os_position_set, Fitness_list, MS, OS,  process_machine):
        """
        :param now_iteration_num: 算法当前迭代次数
        :param ms_position_set: MS的位置信息集合，形式如[[1.3, 2.4, -1.5, ···], [], ···]
        :param os_position_set: OS的位置信息集合，形式如[[1.3, 2.4, -1.5, ···], [], ···]
        :param Fitness_list: 种群的适应度列表，形式如[45, 67, 56, ···]
        :param MS: 机器选择部分编码
        :param OS: 工序排序部分编码
        :param process_machine: 加工机器信息
        :return: ms_position_set为MS更新后的位置信息集合;
                 os_position_set为OS更新后的位置信息集合;
                 Fitness_list为更新后的种群适应度列表;
                 MS为更新后的机器选择部分编码;
                 OS为更新后的工序排序部分编码
        """
        theta = math.pi * now_iteration_num/(10*self.iteration_num)  # 参数θ
        omega = 5   # 参数w
        beta = 1 - round(omega*now_iteration_num/self.iteration_num)/omega
        E = math.sqrt(now_iteration_num/self.iteration_num)  # 附着系数E
        best_individual_idx = Fitness_list.index(min(Fitness_list))
        ms_best_position, os_best_position = ms_position_set[best_individual_idx], os_position_set[best_individual_idx]
        # 软雾凇搜索策略
        if random.random() < E:
            dimension = len(ms_position_set[0])
            new_ms_position_set = [[0 for __ in range(dimension)] for _ in range(self.Pop_size)]
            new_os_position_set = [[0 for __ in range(dimension)] for _ in range(self.Pop_size)]
            for _ in range(self.Pop_size):
                for __ in range(dimension):
                    new_ms = ms_best_position[__] + random.uniform(-1, 1) * math.cos(theta) * beta * \
                             (random.random()*(len(process_machine[__])-1)+1)
                    new_os = os_best_position[__] + random.uniform(-1, 1) * math.cos(theta) * beta * \
                             (random.random()*(len(process_machine[__])-1)+1)
                    new_ms_position_set[_][__], new_os_position_set[_][__] = new_ms, new_os
            new_MS, new_OS = self.location_scheduling_conversion(new_ms_position_set, new_os_position_set, process_machine)
            ms_position_set, os_position_set, Fitness_list, MS, OS = \
                self.update_MS_OS(ms_position_set, os_position_set, new_ms_position_set, new_os_position_set, new_MS, new_OS, Fitness_list, MS, OS)

        # 硬雾凇穿刺机制
        min_fitness, max_fitness = min(Fitness_list), max(Fitness_list)
        # 对适应度进行归一化操作
        if min_fitness == max_fitness:   # 归一化时分母为零的情况，即所有适应度值均相等，此时设置所有适应度归一化之后均为0.5，小概率事件
            normalized_Fitness_list = [0.5 for _ in range(len(Fitness_list))]
        else:
            normalized_Fitness_list = [(Fitness_list[_]-min_fitness)/(max_fitness-min_fitness) for _ in range(len(Fitness_list))]
        for _ in range(self.Pop_size):
            if random.uniform(-1, 1) < normalized_Fitness_list[_]:
                ms_position_set[_] = ms_best_position
                os_position_set[_] = os_best_position
        new_ms_position_set = copy.deepcopy(ms_position_set)
        new_os_position_set = copy.deepcopy(os_position_set)
        new_MS, new_OS = self.location_scheduling_conversion(new_ms_position_set, new_os_position_set, process_machine)
        ms_position_set, os_position_set, Fitness_list, MS, OS = \
            self.update_MS_OS(ms_position_set, os_position_set, new_ms_position_set, new_os_position_set, new_MS,
                              new_OS, Fitness_list, MS, OS)

        return ms_position_set, os_position_set, Fitness_list, MS, OS

    # 主函数
    def main(self):
        """
        主函数，在这完成RIME的各项操作，以及车间的调度
        :return: Optimal_dispatch_scheme:最小完工时间的调度方案;
                         best_fitness: 最小完工时间;
                         best_iteration_fitness: 历次迭代的适应度列表
        """
        MS, OS = Init_Pop(self.Pop_size)
        Pro_Message_set = Decode(MS, OS)
        P_dispatch_set = Dispatch(Pro_Message_set)
        Fitness_list = Fitness(P_dispatch_set)
        ms_position_set, os_position_set = copy.copy(MS), copy.copy(OS)
        best_iteration_fitness = [min(Fitness_list)]
        process_machine = self.machine_message()
        for now_iteration_num in range(1, self.iteration_num+1):
            print(f"第{now_iteration_num}次迭代中....")
            ms_position_set, os_position_set, Fitness_list, MS, OS = \
                self.update_population(now_iteration_num, ms_position_set, os_position_set, Fitness_list, MS, OS, process_machine)
            best_iteration_fitness.append(min(Fitness_list))
        best_fitness = min(best_iteration_fitness)
        ms_best_position = [MS[Fitness_list.index(best_fitness)]]
        os_best_position = [OS[Fitness_list.index(best_fitness)]]

        Pro_Message_set = Decode(ms_best_position, os_best_position)
        P_dispatch_set = Dispatch(Pro_Message_set)
        fitness = Fitness(P_dispatch_set)
        min_time_idx = fitness.index(min(fitness))
        Optimal_dispatch_scheme = P_dispatch_set[min_time_idx]  # 最佳调度方案

        return Optimal_dispatch_scheme, best_fitness, best_iteration_fitness


if __name__ == "__main__":
    Pop_size = 100
    iteration_num = 100
    pro_m, pro_t, J_num, machine_num = Pro_Data()  # 读取加工时间和加工机器的信息
    RIME = RIME(Pop_size, iteration_num)  # 创建ZOA实例，设置种群大小、迭代次数
    Optimal_dispatch_scheme, best_fitness, best_iteration_fitness = RIME.main()
    print(f"\n---------------最最最最佳调度方案---------------")
    for _ in range(len(Optimal_dispatch_scheme)):
        for idx, __ in enumerate(Optimal_dispatch_scheme[_]):
            if idx == 4:
                print(f"{__:>{6}}")
            elif 1 < idx <= 3:
                print(f"{__:>{6}}",end='')
            else:
                print(f"{__:>{3}}", end='')
    print(f"调度总用时为: {best_fitness}")

    Line_Chart(best_iteration_fitness, iteration_num)    # 绘制历次迭代后的适应度
    Gantt(Optimal_dispatch_scheme, best_fitness)  # 绘制甘特图
