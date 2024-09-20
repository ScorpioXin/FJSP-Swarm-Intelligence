from Pro_Data import Pro_Data
from Decode import Decode, Dispatch, Fitness, Single_Decode
from Encode import Init_Pop
from Gantt import Gantt, Line_Chart

import math
import copy
import random
random.seed(15)     # 该种子随机的编码最优解可跑到41second

class PSO_SA:

    def __init__(self, Pop_size, iteration_num, inertia_weight, cognitive_weight,
                 social_weight, pf_max, pf_min, T_start, T_end, B):
        """
        :param Pop_size: 粒子群大小
        :param iteration_num: 迭代次数
        :param inertia_weight: 惯性权重
        :param cognitive_weight: 自我认知权重
        :param social_weight: 社会认知权重
        :param pf_max: RPX算子的最大自适应调整概率
        :param pf_min: RPX算子的最小自适应调整概率
        :param T_start: 初始温度
        :param T_end: 终止温度
        :param B: 退火率
        """
        self.Pop_size = Pop_size                # 粒子群大小
        self.iteration_num = iteration_num      # 迭代次数
        self.w = inertia_weight                 # 惯性权重
        self.c1 = cognitive_weight              # 学习因子(加速常数),自我认知权重
        self.c2 = social_weight                 # 社会认知权重
        self.pf_max = pf_max                    # RPX算子的最大自适应调整概率
        self.pf_min = pf_min                    # RPX算子的最小自适应调整概率
        self.T_start = T_start                  # 初始温度
        self.T_end = T_end                      # 终止温度
        self.B = B                              # 退火率

    def pox_operator(self, single_ms, pBi_ms, single_os, pBi_os):
        """
        POX交叉操作
        :param single_ms: 单条ms染色体
        :param pBi_ms: ms的个体最优染色体
        :param single_os: 单条os染色体
        :param pBi_os: os的个体最优染色体
        :return: Fms：经过pox交叉后的ms；Fos：经过pox交叉后的os
        """
        J1_num = random.randint(1, J_num - 1)                                # 随机生成工件集1中含有的工件数(显然不能把所有的工件都分到工件集1中)
        J1_list = random.sample(range(1, J_num + 1), J1_num)                 # 工件集1的列表
        J2_list = [i for i in range(1, J_num + 1) if i not in J1_list]      # 工件集2的列表(工件集1中没有的工件)
        J = [J1_list, J2_list]
        Fos = [0 for _ in range(0, len(single_os))]     # Fos = [0, 0, 0, 0, 0, ····]
        Fms = [0 for _ in range(0, len(single_ms))]
        for POX_idx, _ in enumerate(single_os):         # single_os = [3, 1, 2, 1, 2, ····]
            if _ in J[0]:
                Fos[POX_idx] = single_os[POX_idx]       # 复制p中属于工件集J中工件的工序到c
                Fms[POX_idx] = single_ms[POX_idx]

        pB_osidx = [POX_idx for POX_idx, _ in enumerate(pBi_os) if _ in J[1]]     # 个体最优pB的位置在工件集2中的索引
        pB_msidx = copy.copy(pB_osidx)
        for idx, _ in enumerate(Fos):
            if _ != 0: pass
            else:
                Fos[idx] = pBi_os[pB_osidx.pop(0)]
                Fms[idx] = pBi_ms[pB_msidx.pop(0)]

        return Fms, Fos

    def rpx_operator(self, single_os, Bi_ms, Bi_os, FXms, FXos, gen):
        """
        RPX交叉操作
        :param single_os: 单条os染色体
        :param Bi_ms: ms的个体最优解(用于f2算子)或全局最优解(用于f3算子)
        :param Bi_os: os的个体最优解(用于f2算子)或全局最优解(用于f3算子)
        :param FXms: 当前进行rpx交叉的ms
        :param FXos: 当前进行rpx交叉的os
        :param gen: 当前的迭代数
        :return: 经过rpx交叉的ms、os
        """
        pf = self.pf_max - (self.pf_max - self.pf_min) / self.iteration_num * gen
        R = [random.random() for _ in range(len(single_os))]
        rpx_idx = [idx for idx, _ in enumerate(R) if _ < pf]
        for _ in range(len(rpx_idx)):
            cut_single_os = single_os[:_+1]
            job_label = single_os[rpx_idx[_]]
            job_order = cut_single_os.count(job_label)
            Bi_idx_list = [idx for idx, _ in enumerate(Bi_os) if _ == job_label]
            Bi_idx = Bi_idx_list[job_order - 1]
            FX_idx_list = [idx for idx, _ in enumerate(FXos) if _ == job_label]
            FX_idx = FX_idx_list[job_order - 1]
            FXms[FX_idx] = Bi_ms[Bi_idx]

        return FXms, FXos

    def PSO_f1_operation(self, single_ms, single_os):   # 传入一对粒子
        single_ms_backup = copy.copy(single_ms)         # 备份
        single_os_backup = copy.copy(single_os)
        two_diff_idx = random.sample(range(0, len(single_os)), 2)
        while single_os[two_diff_idx[0]] == single_os[two_diff_idx[1]]:
            two_diff_idx = random.sample(range(0, len(single_os)), 2)
        fir_gene, sec_gene = single_os[two_diff_idx[0]], single_os[two_diff_idx[1]]      # 获得两个基因对应的工件编号
        before_fir_gene_idx = [idx for idx, _ in enumerate(single_os_backup) if _ == fir_gene]   # 记录交换基因前第一个基因所对应的工件编号出现的所有索引
        before_sec_gene_idx = [idx for idx, _ in enumerate(single_os_backup) if _ == sec_gene]   # 记录交换基因前第二个基因所对应的工件编号出现的所有索引
        single_os[two_diff_idx[0]], single_os[two_diff_idx[1]] = single_os[two_diff_idx[1]], single_os[two_diff_idx[0]]  # 在single_os中交换两个基因
        after_fir_gene_idx = [idx for idx, _ in enumerate(single_os) if _ == fir_gene]   # 记录交换基因后第一个基因所对应的工件编号出现的所有索引
        after_sec_gene_idx = [idx for idx, _ in enumerate(single_os) if _ == sec_gene]   # 记录交换基因后第二个基因所对应的工件编号出现的所有索引
        for _ in range(len(before_fir_gene_idx)):  # 对应调整single_ms,保持各个工序的机器分配不变
            single_ms[after_fir_gene_idx[_]] = single_ms_backup[before_fir_gene_idx[_]]
        for _ in range(len(before_sec_gene_idx)):
            single_ms[after_sec_gene_idx[_]] = single_ms_backup[before_sec_gene_idx[_]]

        random_idx = random.randint(0, len(single_os) - 1)
        cut_single_os = single_os[:random_idx+1]
        job_label = single_os[random_idx]
        job_order = cut_single_os.count(job_label)
        alter_machine_num = len(pro_m[job_label-1][job_order-1])
        if alter_machine_num == 1: pass
        else:
            replace_label = random.randint(1, alter_machine_num)
            while replace_label == single_ms[random_idx]:
                replace_label = random.randint(1, alter_machine_num)
            single_ms[random_idx] = replace_label

        return single_ms, single_os             # 经过f1算子操作，single_ms和single_os对应的就是Eki

    def PSO_f2_operation(self, single_ms, pBi_ms, single_os, pBi_os, gen):
        Fms, Fos = self.pox_operator(single_ms, pBi_ms, single_os, pBi_os)
        single_ms, single_os = self.rpx_operator(single_os, pBi_ms, pBi_os, Fms, Fos, gen)

        return single_ms, single_os             # 经过f2算子操作，single_ms和single_os对应的就是Fki

    def PSO_f3_operator(self, single_ms, gBi_ms, single_os, gBi_os, gen):
        single_ms, single_os = self.rpx_operator(single_os, gBi_ms, gBi_os, single_ms, single_os, gen)

        return single_ms, single_os             # 经过f3算子操作，single_ms和single_os对应的就是Xki

    def SA(self, single_ms, single_os, machine_num):
        T = self.T_start
        fin_single_ms = copy.copy(single_ms)    # 记录每一次退火后的优解位置，后面判断是否更新位置用
        fin_single_os = copy.copy(single_os)

        while T > self.T_end:
            fin_pro_Message = Single_Decode(fin_single_ms, fin_single_os)
            fin_machine_loading = [0 for _ in range(machine_num)]
            for i in fin_pro_Message:
                fin_machine_loading[int(i[2]) - 1] = fin_machine_loading[int(i[2]) - 1] + i[3]
            fin_total_process_time = max(fin_machine_loading)               # 最后一次退火处理时的适应度

            Pro_Message = Single_Decode(single_ms, single_os)      # Pro_Message形式如：[[2, 1, 3.0, 6.0], [2, 2, 2.0, 6.0], [1, 1, 4.0, 3.0], [1, 2, 2.0, 8.0], [2, 3, 5.0, 8.0], ····]
            machine_loading = [0 for _ in range(machine_num)]      # 用于记录机器的负载
            for i in Pro_Message:
                machine_loading[int(i[2]) - 1] = machine_loading[int(i[2]) - 1] + i[3]            # machine_loading形式如：[0, 14.0, 6.0, 3.0, 8.0]
            # print(single_ms)
            # print(single_os)
            # print(machine_loading)
            max_loading_machine_label = machine_loading.index(max(machine_loading)) + 1           # 最大负载机器编号
            # print(max_loading_machine_label)
            machine_label = []
            for _ in range(len(single_ms)):
                cut_os = single_os[:_+1]
                j_label = cut_os[-1]             # 获得当前工件编号
                j_order = cut_os.count(j_label)  # 获得当前工件的工序
                machine_label.append(pro_m[j_label-1][j_order-1][single_ms[_]-1])
            # print(machine_label)
            max_loading_machine_idx = [idx for idx, _ in enumerate(machine_label) if _ == max_loading_machine_label]    # 找到最大负载机器编号在single_ms中的索引
            # print(max_loading_machine_idx)
            # random_idx = random.randint(0, len(max_loading_machine_idx) - 1)
            random_idx = random.choice(max_loading_machine_idx)
            cut_os = single_os[:random_idx+1]
            max_loading_machine_label, max_loading_machine_order = cut_os[-1], cut_os.count(cut_os[-1])     # 随机选择最大负载机器中的一个工件的工序
            # print(max_loading_machine_label, max_loading_machine_order)
            opt_machine_label = pro_m[max_loading_machine_label - 1][max_loading_machine_order - 1]                     # 该工件工序可供选择的机器
            # print(opt_machine_label)
            opt_machine_loading = [machine_loading[opt_machine_label[_]-1] for _ in range(len(opt_machine_label))]      # 获得可供选择机器的负载
            # print(opt_machine_loading)
            opt_min_loading_machine = opt_machine_loading.index(min(opt_machine_loading))      # 获得可选机器中负载最小的机器编号
            # print(opt_min_loading_machine)
            single_ms[random_idx] = opt_min_loading_machine + 1            # 替换该工序的机器为可选机器中负载最小的机器
            # print(single_os)
            # print(single_ms)

            opt_Pro_Message = Single_Decode(single_ms, single_os)      # 经过SA处理后的调度信息
            opt_machine_loading = [0 for _ in range(machine_num)]      # 用于记录经过SA处理后机器的负载
            for i in opt_Pro_Message:
                opt_machine_loading[int(i[2]) - 1] = opt_machine_loading[int(i[2]) - 1] + i[3]
            after_total_process_time = max(machine_loading)              # SA处理后的加工时间

            delta = after_total_process_time - fin_total_process_time
            if delta < 0:                       # 如果delta小于零，那么直接接受新解
                fin_single_ms, fin_single_os = single_ms, single_os
            elif delta >= 0:                      # 如果delta不小于零，那么就以概率接受新解
                po = random.uniform(0, 1)
                if po < math.exp(-delta/T):
                    fin_single_ms, fin_single_os = single_ms, single_os

            T = self.B * T          # 以退火率B逐渐退火

        return fin_single_ms, fin_single_os

    def main(self):
        MS, OS = Init_Pop(self.Pop_size)     # 种群初始化

        # 获得个体最优解和整体最优解
        ms_individual_optimal = copy.deepcopy(MS)                             # 初始情况下，个体最优列表就是本身
        os_individual_optimal = copy.deepcopy(OS)
        individual_optimal_message_set = Decode(ms_individual_optimal, os_individual_optimal)
        individual_optimal_dispatch_set = Dispatch(individual_optimal_message_set)
        individual_optimal_fitness_list = Fitness(individual_optimal_dispatch_set)       # 个体最优适应度列表
        global_optimal_idx = individual_optimal_fitness_list.index(min(individual_optimal_fitness_list))   # 获得整体最优解的索引
        global_optimal_fitness = min(individual_optimal_fitness_list)                    # 整体最优的适应度
        ms_global_optimal = ms_individual_optimal[global_optimal_idx]                    # 获得整体最优解：p_gj(t), 形式如[2, 1, 2, 3, 2]
        os_global_optimal = os_individual_optimal[global_optimal_idx]

        fitness_iteration = []    # 历次迭代的适应度
        Optimal_Message_scheme = []
        Pro_Message = Single_Decode(ms_global_optimal, os_global_optimal)
        Optimal_Message_scheme.append(Pro_Message)
        dispatch_scheme = Dispatch(Optimal_Message_scheme)  # 获得最新调度列表集
        Optimal_dispatch_scheme = dispatch_scheme[0]
        fitness = Fitness(dispatch_scheme)  # 适应度计算
        fitness_iteration.append(min(fitness))

        iteration_count = 0
        for _ in range(0, self.iteration_num):
            # individual_optimal_message_set = Decode(ms_individual_optimal, os_individual_optimal)
            # individual_optimal_dispatch_set = Dispatch(individual_optimal_message_set)
            # individual_optimal_fitness_list = Fitness(individual_optimal_dispatch_set)       # 个体最优适应度列表
            # global_optimal_fitness = min(individual_optimal_fitness_list)                    # 整体最优的适应度

            iteration_count += 1
            print(f"第{iteration_count}次迭代中....")
            for __ in range(len(MS)):
                single_ms, single_os = MS[__], OS[__]

                # 执行DPSO算法
                pr = random.random()               # 随机生成一个概率
                if pr < self.w:                    # 判断是否执行PSO的f1算子
                    single_ms, single_os = self.PSO_f1_operation(single_ms, single_os)
                pr = random.random()
                if pr < self.c1:                   # 判断是否执行PSO的f2算子
                    single_ms, single_os = self.PSO_f2_operation(single_ms, ms_individual_optimal[__], single_os, os_individual_optimal[__], iteration_count)
                pr = random.random()
                if pr < self.c2:                   # 判断是否执行PSO的f3算子
                    single_ms, single_os = self.PSO_f3_operator(single_ms, ms_global_optimal, single_os, os_global_optimal, iteration_count)

                # 执行SA算法(用于局部领域搜索，含有接受较差解的概率)
                single_ms, single_os = self.SA(single_ms, single_os, machine_num)

                MS[__], OS[__] = single_ms, single_os         # 更新粒子位置

            # 判断是否更新个体最优和全局最优
            now_message_set = Decode(MS, OS)  # 当前粒子群位置对应的加工信息集
            now_dispatch_set = Dispatch(now_message_set)  # 当前粒子群位置对应的调度信息集
            now_fitness_list = Fitness(now_dispatch_set)  # 当前粒子群位置对应的适应度列表
            now_fitness_optimal = min(now_fitness_list)   # 当前粒子群位置中适应度最优的大小
            for i in range(len(now_fitness_list)):  # 处理是否更新个体最优解
                if individual_optimal_fitness_list[i] < now_fitness_list[i]:  # 当前粒子位置劣于它的历史最佳位置，不更新
                    pass
                elif individual_optimal_fitness_list[i] > now_fitness_list[i]:  # 当前粒子位置优于它的历史最佳位置，更新
                    ms_individual_optimal[i] = copy.copy(MS[i])
                    os_individual_optimal[i] = copy.copy(OS[i])
                elif now_fitness_list[i] == individual_optimal_fitness_list[i]:  # 当前粒子位置与它的历史最佳位置同样优秀，以50%的概率判断是否更新
                    update_p = random.uniform(0, 1)
                    if update_p >= 0.5:  # 如果随机产生的更新概率不小于0.5，那么更新个体最优解列表
                        ms_individual_optimal[i] = copy.copy(MS[i])
                        os_individual_optimal[i] = copy.copy(OS[i])

            if global_optimal_fitness < now_fitness_optimal:  # 整体最优适应度比当前粒子群的最优适应度都要好，不更新
                pass
            elif global_optimal_fitness > now_fitness_optimal:  # 整体最优适应度比当前粒子群的最优适应度要劣，更新
                ms_global_optimal = copy.copy(MS[now_fitness_list.index(now_fitness_optimal)])
                os_global_optimal = copy.copy(OS[now_fitness_list.index(now_fitness_optimal)])
            elif global_optimal_fitness == now_fitness_optimal:  # 整体最优适应度与当前粒子群的最优适应度同样优秀，以50%的概率判断是否更新
                update_p = random.uniform(0, 1)
                if update_p >= 0.5:
                    ms_global_optimal = copy.copy(MS[now_fitness_list.index(now_fitness_optimal)])
                    os_global_optimal = copy.copy(OS[now_fitness_list.index(now_fitness_optimal)])

            Optimal_Message_scheme = []
            Pro_Message = Single_Decode(ms_global_optimal, os_global_optimal)
            Optimal_Message_scheme.append(Pro_Message)
            dispatch_scheme = Dispatch(Optimal_Message_scheme)  # 获得最新调度列表集
            Optimal_dispatch_scheme = dispatch_scheme[0]
            fitness = Fitness(dispatch_scheme)                  # 适应度计算
            fitness_iteration.append(min(fitness))
            global_optimal_fitness = min(fitness_iteration)     # 整体最优的适应度

        return Optimal_dispatch_scheme, min(fitness), fitness_iteration, self.iteration_num

if __name__ == "__main__":
    pro_m, pro_t, J_num, machine_num = Pro_Data()           # 读取加工时间和加工机器的信息
    # 设置粒子群大小、迭代次数、惯性权重、自我认知权重、社会认知权重、最大自适应调整概率、最小自适应调整概率、初始温度、终止温度、退火率
    pso_sa = PSO_SA(50, 50, 0.6, 0.6, 0.6, 0.9, 0.2, 3, 1, 0.9)       # 最优42 or 41
    Optimal_dispatch_scheme, fitness, fitness_iter_list, iteration_num = pso_sa.main()
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

    Line_Chart(fitness_iter_list, iteration_num)    # 绘制历次迭代后的适应度
    Gantt(Optimal_dispatch_scheme, fitness)         # 绘制甘特图