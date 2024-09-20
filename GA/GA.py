import time

from Pro_Data import Pro_Data
from Decode import Init_Pop, Decode, Dispatch, Fitness
from Gantt import Gantt, Line_Chart

import numpy as np
import copy
import random
random.seed(10)

class GA:
    """
    GA类：交叉、变异、选择、主函数
    形参：种群大小：Pop_size ； 交叉概率：Pc ；变异概率：Pm ； 迭代次数：iteration_num ； GLR概率
    """

    def __init__(self, Pop_size, Pc, Pm, iteration_num, GS_P, LS_P, RS_P):
        self.Pc = Pc                            # 交叉概率
        self.Pm = Pm                            # 变异概率
        self.Pop_size = Pop_size                # 种群大小
        self.iteration_num = iteration_num      # 迭代次数
        self.GS_P = GS_P                        # 全局选择概率
        self.LS_P = LS_P                        # 局部选择概率
        self.RS_P = RS_P                        # 随机选择概率

        #用于另一种交叉和变异方式：通过循环，直到达到交叉、循环次数(缺点：交叉次数和变异次数可能过多，不太可控)
        # self.Pop_C_num = round(Pc * Pop_size)   #交叉次数
        # self.Pop_M_num = round(Pm * Pop_size)   #变异次数

    #交叉
    def Crossover(self, MS, OS):
        """
        :param MS: 需要交叉的机器选择部分的染色体(一对)，形式如[[1,2,3,···],[2,2,1,···]]
        :param OS: 需要交叉的工序选择部分的染色体(一对)，形式如[[1,2,1,···],[2,1,1,···]]
        :return: 交叉完的MS和OS
        """
        # 机器选择部分交叉(均匀交叉)
        crossover_num = random.randint(1, len(MS[0]))  # 不交叉次数
        crossover_idx = random.sample(range(0, len(MS[0])), crossover_num)  # 获得基因交叉位置的索引,#crossover_idx = [2, 4]
        MS = np.array(MS)  # 列表转数组处理
        CMS = [[0 for _ in range(0, len(MS[__]))] for __ in range(0, len(MS))]  # 初始化子代的MS

        for _ in range(0, len(MS)):  # len(MS)=2
            for __ in range(0, len(MS[_])):  # len(MS[_])=5
                if __ in crossover_idx:  # 索引位需要交叉
                    CMS[_][__] = MS[_][__]
            for __ in range(0, len(MS[_])):
                if __ not in crossover_idx:  # 索引位不需要交叉
                    CMS[0][__] = MS[1][__]
                    CMS[1][__] = MS[0][__]

        # 工序排序部分交叉(POX交叉)
        J1_num = random.randint(1,J_num - 1)                                #随机生成工件集1中含有的工件数(显然不能把所有的工件都分到工件集1中)
        J1_list = random.sample(range(1, J_num + 1),J1_num)                 #工件集1的列表
        J2_list = [i for i in range(1, J_num + 1) if i not in J1_list]      #工件集2的列表(工件集1中没有的工件)
        J = [J1_list, J2_list]
        # J = [[1], [2, 3]]  # 划分工件集
        COS = [[0 for _ in range(0, len(OS[__]))] for __ in range(0, len(OS))]
        for _ in range(0, len(OS)):  # OS = [[3, 1, 2, 1, 2], [1, 2, 1, 2, 3]]
            for POX_idx, __ in enumerate(OS[_]):
                if __ in J[0]:
                    COS[_][POX_idx] = OS[_][POX_idx]  # 复制p中属于工件集J中工件的工序到c
        P1_idx = [POX_idx for POX_idx, _ in enumerate(OS[0]) if _ not in J[0]]  # 获得不在工件集J1中的索引
        P2_idx = [POX_idx for POX_idx, _ in enumerate(OS[1]) if _ not in J[0]]

        for idx, _ in enumerate(COS[0]):
            if _ != 0:
                pass
            else:
                COS[0][idx] = OS[1][P2_idx.pop(0)]

        for idx, _ in enumerate(COS[1]):
            if _ != 0:
                pass
            else:
                COS[1][idx] = OS[0][P1_idx.pop(0)]

        MS = CMS  # 子代为下一轮的父代
        OS = COS
        return MS, OS

    #变异
    def Mutation(self, MS):
        """
        :param MS: 需要变异的机器选择部分染色体(一个)，形式如：[2,3,1,···]
        :return: 变异后的MS
        """
        #机器选择部分
        restruct_pro_t = []
        for i in range(len(pro_t)):         #重构列表pro_t ,方便处理
            for j in range(len(pro_t[i])):
                restruct_pro_t.append(pro_t[i][j])

        # for _ in range(0, len(MS)):
        mutation_num = random.randint(1, len(MS))  # 变异基因数
        mutation_idx = random.sample(range(0, len(MS)), mutation_num)  # 变异位置索引列表
        mutation_idx.sort()
        for idx, __ in enumerate(MS):
            if idx in mutation_idx:
                # 查找加工时间最短的机器
                mut_idx = mutation_idx.pop(0)  # MS变异位置
                min_time = min(restruct_pro_t[mut_idx])
                min_time_idx = restruct_pro_t[mut_idx].index(min_time)
                MS[mut_idx] = min_time_idx + 1       # 将变异位置改成当前工序加工时间最小的机器的顺序编号（非机器编号）
            else:
                pass
        return MS

    #选择
    def Selection(self, P_dispatch_set, CMS, COS, Pop_Crossover_set):
        """
        :param P_dispatch_set: 加工数据集
        :param CMS: 种群交叉池的机器选择部分染色体编码
        :param COS: 种群交叉池的工序排序部分染色体编码
        :param Pop_Crossover_set: 未更新的种群交叉池
        :return: 更新后的CMS, COS, Pop_Crossover_set
        """
        MS = CMS
        OS = COS
        Cross_set_fitness = Fitness(Pop_Crossover_set)
        Pop_set_fitness = Fitness(P_dispatch_set)
        for _ in range(3):                              # 设置选择次数的上限，不超过染色体长度(每次选择的染色体不重复)
            # print(f"\n第{_ + 1}次选择前")
            # print(f"当前种群的适应度列表:{Pop_set_fitness}")
            # print(f"交叉池的适应度列表:{Cross_set_fitness}")
            if max(Cross_set_fitness) <= min(Pop_set_fitness):
                pass  # 已经达到最优
            else:
                C_idx = Cross_set_fitness.index(max(Cross_set_fitness))
                P_idx = Pop_set_fitness.index(min(Pop_set_fitness))
                CMS[C_idx] = MS[P_idx]                      # 将CMS中最劣的染色体替换成最优的染色体(更新交叉池)
                COS[C_idx] = OS[P_idx]
                Pop_Crossover_set[C_idx] = P_dispatch_set[P_idx]  # 更新交叉池中的种群调度信息
                Cross_set_fitness[C_idx] = 0            # 已经选择过的染色体索引位作"极限"处理
                Pop_set_fitness[P_idx] = 9999

        return CMS, COS, Pop_Crossover_set

    #主函数
    def main(self):
        """
        主函数，在这完成GA的各项操作，以及车间的调度
        :return: 最小完工时间的调度方案：Optimal_dispatch_scheme, 形式如[[工件, 工序, 机器, 开始加工时间, 结束加工时间], [6, 1, 6.0, 3.0, 5.0],···] ;
        最小加工时间：min(fitness)
        历次迭代的最优适应度列表：best_iteration_fitness
        """
        Pop_Crossover_set = []                              # 给个初始化，避免赋值前被引用
        Optimal_dispatch_scheme = []
        CMS = []
        COS = []

        init_crossover_set_flag = True                      # 初始化交叉池参数的标记
        MS, OS = Init_Pop(self.Pop_size, self.GS_P, self.LS_P, self.RS_P)     # 种群初始化, 设置GLR比例

        Pro_Message_set = Decode(MS, OS)
        P_dispatch_set = Dispatch(Pro_Message_set)
        Fitness_list = Fitness(P_dispatch_set)
        best_iteration_fitness = [min(Fitness_list)]
        for _ in range(self.iteration_num):                 # 开始迭代
            print(f"第{_+1}次迭代中")
            Pro_Message_set = Decode(MS, OS)                # MS、OS染色体解码
            P_dispatch_set = Dispatch(Pro_Message_set)      # 获得调度列表集
            if init_crossover_set_flag == True:             # 初始化交叉池只需要执行一次
                Pop_Crossover_set = copy.deepcopy(P_dispatch_set)          # 初始交叉池为初始种群的各项信息
                CMS = MS
                COS = OS
                init_crossover_set_flag = False

            # 选择
            CMS, COS, Pop_Crossover_set = G.Selection(P_dispatch_set, CMS, COS, Pop_Crossover_set)  # 选择操作

            # 交叉
            # for i in range(self.Pop_C_num):                         #循环交叉，直到达到交叉次数(另一种交叉方式)
            Pc_random = random.random()
            if Pc_random <= self.Pc:  # 判断是否交叉(比较随机产生的概率与Pc的值)
                idx_list = [j for j in range(len(CMS))]  # 获得所有染色体的索引
                crossover_idx_list = random.sample(idx_list, 2)  # 随机选择两个不同染色体的索引，这两个索引对应的染色体便是交叉对象
                M_crossover_list = [CMS[crossover_idx_list[0]],
                                    CMS[crossover_idx_list[1]]]  # M_crossover_list含用于交叉的两个染色体(MS部分)
                O_crossover_list = [COS[crossover_idx_list[0]],
                                    COS[crossover_idx_list[1]]]  # O_crossover_list含用于交叉的两个染色体(OS部分)
                cms, cos = G.Crossover(M_crossover_list, O_crossover_list)  # 交叉操作
                for j in range(2):
                    CMS[crossover_idx_list[j]] = cms[j]  # 交叉完的染色体替换掉交叉池对应位置的染色体
                    COS[crossover_idx_list[j]] = cos[j]

            # 变异(另一种方式)
            # mutation_idx = None                                     #初始化随机获得的变异染色体的索引
            # already_mutation = []                                   #用于记录已经变异过的染色体，每次迭代中每个染色体仅能变异至多一次
            # for i in range(self.Pop_M_num):                         #循环变异，直到达到变异次数(另一种变异方式)
            #     while mutation_idx in already_mutation:             #循环找到没有变异过的染色体索引位
            #         mutation_idx = random.randint(0,len(CMS)-1)     #随机选择一个染色体的索引，这个索引对应的染色体便是变异对象
            #     cms = G.Mutation(CMS[mutation_idx], pro_t)  # 变异操作
            #     CMS[mutation_idx] = cms  # 变异完的染色体替换掉交叉池对应位置的染色体

            # 变异
            Pm_random = random.random()
            if Pm_random <= self.Pm:
                mutation_idx = random.randint(0, len(CMS) - 1)  # 随机选择一个染色体的索引，这个索引对应的染色体便是变异对象
                cms = G.Mutation(CMS[mutation_idx])  # 变异操作
                CMS[mutation_idx] = cms  # 变异完的染色体替换掉交叉池对应位置的染色体

            Pro_Message_set = Decode(CMS, COS)              # CMS、COS染色体解码
            P_dispatch_set = Dispatch(Pro_Message_set)      # 获得调度列表集
            fitness = Fitness(P_dispatch_set)               # 适应度计算
            min_time_idx = fitness.index(min(fitness))      # 获得适应度最高(最小加工时间)的索引
            Optimal_dispatch_scheme = P_dispatch_set[min_time_idx]     # 最佳调度方案

            best_iteration_fitness.append(min(fitness))

        # 方案会重复输出
        # print(f'比较优的调度方案：')
        # for i in range(len(P_dispatch_set)):
        #     print(f"---------------第{i + 1}种调度方案---------------"
        #           f"\n{P_dispatch_set[i]}"
        #           f"\n用时为：{fitness[i]}")

        # 方案不重复输出
        scheme_count = 1                                         # 记录是第几个方案
        print_dispatch_scheme = []                              # 记录已经输出过的方案
        print(f'最后一次迭代产生的不重复调度方案：')
        for i in range(len(P_dispatch_set)):
            if P_dispatch_set[i] not in print_dispatch_scheme:     # 如果没有输出过该方案
                print(f"---------------第{scheme_count}种调度方案---------------"
                      f"\n{P_dispatch_set[i]}"
                      f"\n用时为：{fitness[i]}")
                print_dispatch_scheme.append(P_dispatch_set[i])
                scheme_count += 1
            else: pass

        # print(Pro_Message_set[min_time_idx])                      #输出的Pro_Message_set[min_time_idx]用于测试调度方案
        return Optimal_dispatch_scheme, min(fitness), best_iteration_fitness

if __name__ == "__main__":
    '''
    mk01问题：
    当GLR比例为 1:0:0 , 种群大小为200, 交叉概率为0.8, 变异概率为0.3, 迭代次数为100时可达到局部最优解: 42
    当GLR比例为 0.8:0.1:0.1 , 种群大小为100, 交叉概率为0.8, 变异概率为0.3, 迭代次数为100时可达到局部最优解: 42    
    
    检查调度方案是否正确：
    ①查看所有机器的时间线是否重叠，无重叠则正确；
    ②检查所有工件的加工时间是否满足工序的约束，满足则正确。
    '''
    stime = time.time()
    Pop_size = 100
    Pm = 0.8
    Pc = 0.3
    iteration_num = 100
    G, L, R = 0.8, 0.1, 0.1
    pro_m, pro_t, J_num, machine_num = Pro_Data()   # 读取加工时间和加工机器的信息
    G = GA(Pop_size, Pm, Pc, iteration_num, G, L, R)      # 创建GA实例，设置种群大小、交叉概率、变异概率、迭代次数和GLR的概率
    Optimal_dispatch_scheme, fitness, best_iteration_fitness = G.main()
    print(f'算法迭代用时为：{time.time()-stime}')

    print(f"\n---------------最最最最佳调度方案---------------")
    for _ in range(len(Optimal_dispatch_scheme)):
        for idx, __ in enumerate(Optimal_dispatch_scheme[_]):
            if idx == 4:
                print(f"{__:>{6}}")
            elif 1 < idx <= 3:
                print(f"{__:>{6}}",end='')
                # print(__,end='  ')
            else:
                print(f"{__:>{3}}", end='')
    print(f"用时为: {fitness}")

    Line_Chart(best_iteration_fitness, iteration_num)
    Gantt(Optimal_dispatch_scheme, fitness)          # 绘制甘特图