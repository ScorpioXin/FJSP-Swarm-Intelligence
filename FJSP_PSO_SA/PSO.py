from Pro_Data import Pro_Data
from Decode import Init_Pop,Decode,Dispatch,Fitness
from Gantt import Gantt

import numpy as np
import heapq
import copy
import random
random.seed(8)

class PSO:
    """
    PSO类：粒子群，主要处理粒子的速度和位置
    传参：Pop_size：粒子群大小 ; iteration_num: 迭代次数 ; weight: 惯性权重
        c1、c2: 学习因子(加速常数),代表了当前粒子受个体最优粒子位置与全局最优粒子位置的影响程度
        GS_P, LS_P, RS_P：GLR概率
    """

    def __init__(self, Pop_size, iteration_num, inertia_weight, cognitive_weight, social_weight, GS_P, LS_P, RS_P):
        """
        :param Pop_size: 粒子群大小
        :param iteration_num: 迭代次数
        :param inertia_weight: 惯性权重
        :param cognitive_weight: 自我认知权重
        :param social_weight: 社会认知权重
        :param GS_P: 全局选择概率
        :param LS_P: 局部选择概率
        :param RS_P: 随机选择概率
        """
        self.Pop_size = Pop_size                # 粒子群大小
        self.iteration_num = iteration_num      # 迭代次数
        self.w = inertia_weight                 # 惯性权重
        self.c1 = cognitive_weight              # 学习因子(加速常数),自我认知权重
        self.c2 = social_weight                 # 社会认知权重
        self.max_velocity = 2                   # 最大速度设置
        self.min_velocity = -2
        self.GS_P = GS_P                        # 全局选择概率
        self.LS_P = LS_P                        # 局部选择概率
        self.RS_P = RS_P                        # 随机选择概率

    def init_velocity(self, MS):
        """
        初始化粒子的速度
        :return: 粒子的初速度velocity，形式如[[1, 2, 0, 2, 1], [2, -2, 1, 0, -2], [-2, 2, -2, -2, 0], ····]
        """
        velo_list = [[random.randint(self.min_velocity, self.max_velocity) for __ in range(len(MS[_]))] for _ in range(len(MS))]  # 初始化速度
        return velo_list

    # 先处理MS，后期处理OS
    def pso(self, MS, OS, velo_list, ms_individual_optimal, os_individual_optimal):
        """
        :param MS: 机器选择部分编码
        :param OS: 工序排序部分编码
        :param velo_list: 粒子的初速度列表，形式如[[1, 2, 0, 2, 1], [2, -2, 1, 0, -2],····]
        :param ms_individual_optimal: 机器选择部分的个体最优，形式如[[2, 1, 2, 3, 2], [5, 1, 3, 2, 4],····]
        :param os_individual_optimal: 工序排序部分的个体最优，形式如[[1, 1, 2, 2, 2], [2, 2, 2, 1, 1],····]
        :return: Optimal_dispatch_scheme:最佳调度方案
                 min(fitness)：最优适应度
        """
        alter_velo = [_ for _ in range(self.min_velocity, self.max_velocity + 1)]       # 速度可选列表，形式如：[-2, -1, 0, 1, 2]
        sequence_os = copy.deepcopy(OS[0])
        sequence_os.sort()                      # 获得顺序排序的工件列表(是个一维列表，形式如[1,1,2,2,2])

        # 先获得个体最优解和整体最优解
        individual_optimal_message_set = Decode(ms_individual_optimal, os_individual_optimal)
        individual_optimal_dispatch_set = Dispatch(individual_optimal_message_set)
        individual_optimal_fitness_list = Fitness(individual_optimal_dispatch_set)       # 个体最优适应度列表
        global_optimal_idx = individual_optimal_fitness_list.index(min(individual_optimal_fitness_list))   # 获得整体最优解的索引
        global_optimal_fitness = min(individual_optimal_fitness_list)                    # 整体最优的适应度
        ms_global_optimal = ms_individual_optimal[global_optimal_idx]                    # 获得整体最优解：p_gj(t), 形式如[2, 1, 2, 3, 2]
        os_global_optimal = os_individual_optimal[global_optimal_idx]

        ms_real_position = 0
        real_velo_idx = 0
        for _ in range(len(MS)):
            J_appear = []
            for idx, __ in enumerate(MS[_]):
                r1 = random.uniform(0, 1)                                # 为更新速度和位置引入随机性，生成[0,1]之间的随机数
                r2 = random.uniform(0, 1)
                velo_list[_][idx] = self.w * velo_list[_][idx] + self.c1 * r1 * (ms_individual_optimal[_][idx] - __) + \
                                    self.c2 * r2 * (ms_global_optimal[idx] - __)
                velo_list[_][idx] = round(velo_list[_][idx])             # 离散速度，取整处理
                if abs(velo_list[_][idx]) <= self.max_velocity:          # 速度并未越界
                    pass
                else:                                                    # 越界
                    # 处理方式1：越界后再随机生成一个合理速度
                    # velo_list[_][idx] = round(random.uniform(self.min_velocity, self.max_velocity))

                    # 处理方式2：可选速度列表循环使用
                    if velo_list[_][idx] >= 0 and ((velo_list[_][idx] - self.max_velocity) % len(alter_velo)) != 0:
                        real_velo_idx = ((velo_list[_][idx] - self.max_velocity) % len(alter_velo)) - 1
                    elif velo_list[_][idx] >= 0 and ((velo_list[_][idx] - self.max_velocity) % len(alter_velo)) == 0:
                        real_velo_idx = len(alter_velo) - 1                                     # 正序整除，正速度最大
                    elif velo_list[_][idx] < 0 and ((velo_list[_][idx] - self.min_velocity) % len(alter_velo)) != 0:
                        real_velo_idx = (velo_list[_][idx] - self.min_velocity) % len(alter_velo)
                    elif velo_list[_][idx] < 0 and ((velo_list[_][idx] - self.min_velocity) % len(alter_velo)) == 0:
                        real_velo_idx = 0                                                       # 逆序整除，负速度最大
                    velo_list[_][idx] = alter_velo[real_velo_idx]

                # MS移动部分
                ms_new_position = __ + velo_list[_][idx]
                J = sequence_os[idx]
                J_appear.append(J)
                column = J_appear.count(J)                          # 工件的工序
                alter_machine_num = len(pro_m[J-1][column-1])       # 可选机器的数量
                if abs(ms_new_position) <= alter_machine_num:       # 并未越界
                    if ms_new_position == 0:
                        pass
                    elif ms_new_position > 0:                          # 正序位置(正序选择机器编号)
                        MS[_][idx] = ms_new_position                   # 更新粒子的位置
                    else:                                              # 逆序位置
                        MS[_][idx] = alter_machine_num - abs(ms_new_position)
                else:                                                  # 越界
                    if ms_new_position >= 0 and (ms_new_position % alter_machine_num) != 0:
                        ms_real_position = (ms_new_position % alter_machine_num)                # 保证不会越界的真实位置
                    elif ms_new_position >= 0 and (ms_new_position % alter_machine_num) == 0:
                        ms_real_position = alter_machine_num                                    # 顺序情况下整除，选最后一台机器
                    elif ms_new_position < 0 and (abs(ms_new_position) % alter_machine_num) != 0:
                        ms_real_position = (ms_new_position % alter_machine_num) + 1
                        # real_position = alter_machine_num - (abs(new_position) % alter_machine_num) + 1
                    elif ms_new_position < 0 and (abs(ms_new_position) % alter_machine_num) == 0:
                        ms_real_position = 1                                                    # 逆序情况下整除，选择第一台机器
                    MS[_][idx] = ms_real_position

                #OS移动部分
                velo_list[_][idx] = self.w * velo_list[_][idx] + self.c1 * r1 * (ms_individual_optimal[_][idx] - __) + \
                                    self.c2 * r2 * (ms_global_optimal[idx] - __)
                os_new_position = OS[_][idx] + velo_list[_][idx]         # OS未整数处理前的新位置
                virtual_os = copy.deepcopy(OS)
                virtual_os[_][idx] = os_new_position                     # 形式如[[1.5,2.2,3.0,···],[-1,5.2,-3.5,···],····]
            # 等这个粒子的所有维度坐标都确定后才对OS的处理
            for idx, i in enumerate(virtual_os[_]):
                virtual_os[_][idx] = round(i, 3)
            job_label = set(sequence_os)            # 获得工件号，形式如: {1,2,3,····}
            for i in job_label:
                h_num = sequence_os.count(i)        # 工件i所含工序数h
                min_value__list = heapq.nsmallest(h_num, virtual_os[_])        # 获得与当前工件工序数相等的前几个最小值
                for j in range(h_num):
                    min_value_idx = virtual_os[_].index(min_value__list[j])
                    OS[_][min_value_idx] = i
                    virtual_os[_][min_value_idx] = 999                         # 已经访问过的索引取相对的极限处理

        # 判断是否更新个体最优解和全局最优解
        now_message_set = Decode(MS, OS)                    # 当前粒子群位置对应的加工信息集
        now_dispatch_set = Dispatch(now_message_set)        # 当前粒子群位置对应的调度信息集
        now_fitness_list = Fitness(now_dispatch_set)        # 当前粒子群位置对应的适应度列表
        now_fitness_optimal = min(now_fitness_list)         # 当前粒子群位置中适应度最优的大小
        for _ in range(len(now_fitness_list)):              # 处理是否更新个体最优解
            if individual_optimal_fitness_list[_] < now_fitness_list[_]:          # 当前粒子位置劣于它的历史最佳位置，不更新
                pass
            elif individual_optimal_fitness_list[_] > now_fitness_list[_]:        # 当前粒子位置优于它的历史最佳位置，更新
                ms_individual_optimal[_] = copy.copy(MS[_])
                os_individual_optimal[_] = copy.copy(OS[_])
            elif now_fitness_list[_] == individual_optimal_fitness_list[_]:       # 当前粒子位置与它的历史最佳位置同样优秀，以50%的概率判断是否更新
                update_p = random.uniform(0, 1)
                if update_p >= 0.5:                                   # 如果随机产生的更新概率不小于0.5，那么更新个体最优解列表
                    ms_individual_optimal[_] = copy.copy(MS[_])
                    os_individual_optimal[_] = copy.copy(OS[_])
                else: pass

        if global_optimal_fitness < now_fitness_optimal:              # 整体最优适应度比当前粒子群的最优适应度都要好，不更新
            pass
        elif global_optimal_fitness > now_fitness_optimal:            # 整体最优适应度比当前粒子群的最优适应度要劣，更新
            ms_global_optimal = copy.copy(MS[now_fitness_list.index(now_fitness_optimal)])
            os_global_optimal = copy.copy(OS[now_fitness_list.index(now_fitness_optimal)])
        elif global_optimal_fitness == now_fitness_optimal:           # 整体最优适应度与当前粒子群的最优适应度同样优秀，以50%的概率判断是否更新
            update_p = random.uniform(0, 1)
            if update_p >= 0.5:
                ms_global_optimal = copy.copy(MS[now_fitness_list.index(now_fitness_optimal)])
                os_global_optimal = copy.copy(OS[now_fitness_list.index(now_fitness_optimal)])
            else: pass

        return MS, OS, velo_list, ms_individual_optimal, os_individual_optimal, ms_global_optimal, os_global_optimal


    def main(self):
        MS, OS = Init_Pop(self.Pop_size, self.GS_P, self.LS_P, self.RS_P)     # 种群初始化, 设置GLR比例
        velo_list = self.init_velocity(MS)
        ms_individual_optimal = copy.deepcopy(MS)                             # 初始情况下，个体最优列表就是本身
        os_individual_optimal = copy.deepcopy(OS)

        # init_Message_set = Decode(MS, OS)
        # init_dispatch_set = Dispatch(init_Message_set)  # 获得调度列表集
        # init_fitness_list = Fitness(init_dispatch_set)
        # fitness = copy.copy(init_fitness_list)
        iteration_count = 1
        for _ in range(0, self.iteration_num):
        # while min(fitness) >= 53:
            print(f"第{iteration_count}次迭代中....")
            MS, OS, velo_list, ms_individual_optimal, os_individual_optimal, ms_global_optimal, os_global_optimal = \
                self.pso(MS, OS, velo_list, ms_individual_optimal, os_individual_optimal)
            iteration_count += 1

        Optimal_MS = [ms_global_optimal]
        Optimal_OS = [os_global_optimal]
        Optimal_Message_scheme = Decode(Optimal_MS, Optimal_OS)
        dispatch_scheme = Dispatch(Optimal_Message_scheme)             # 获得调度列表集
        Optimal_dispatch_scheme = dispatch_scheme[0]
        fitness = Fitness(dispatch_scheme)                             # 适应度计算

        return Optimal_dispatch_scheme, min(fitness)

if __name__ == "__main__":
    pro_m, pro_t, J_num, machine_num = Pro_Data()           # 读取加工时间和加工机器的信息
    pso = PSO(30, 100, 0.9, 2, 2, 0, 0, 1)               # 分别设置粒子群大小，迭代次数，惯性权重，自我认知权重，社会认知权重，GLR概率
    Optimal_dispatch_scheme, fitness = pso.main()

    # print(f"\n---------------最佳调度方案---------------")
    # for _ in range(len(Optimal_dispatch_scheme)):
    #     for idx, __ in enumerate(Optimal_dispatch_scheme[_]):
    #         if idx == 4:
    #             print(f"{__:>{6}}")
    #         elif 1 < idx <= 3:
    #             print(f"{__:>{6}}",end='')
    #             # print(__,end='  ')
    #         else:
    #             print(f"{__:>{3}}", end='')
    print(f"用时为: {fitness}")

    # Gantt(Optimal_dispatch_scheme, fitness)  # 绘制甘特图