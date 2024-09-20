from Pro_Data import Pro_Data

import numpy as np


#染色体解码
def Decode(MS,OS):
    """
    所有染色体解码
    :param MS: 机器选择部分编码
    :param OS: 工序排序部分编码
    :return:  加工数据集(Pro_Message_set)：三维列表，形式如[[[],[],···,[]],[[],[],···,[]],···,[[],[],···,[]]] ;
    最内层形式：[工件，工序，加工机器，加工时间]
    """
    # OS = [[2, 1, 2, 1, 2], [2, 1, 2, 1, 2], [1, 1, 2, 2, 2], [2, 2, 1, 2, 1], [1, 2, 2, 1, 2]]
    # MS = [[2, 4, 2, 2, 4], [2, 2, 1, 2, 4], [3, 1, 1, 2, 4], [3, 1, 4, 2, 1], [4, 3, 1, 1, 4]]

    pro_m, pro_t, J_num, machine_num = Pro_Data()
    # 对机器选择部分进行解码
    M_matrix_set = []
    T_matrix_set = []
    J_num = len(pro_t)                      # 工件个数
    O_num = []
    for i in range(len(pro_t)):
        O_num.append(len(pro_t[i]))         # 存储每个工件的工序数
    max_O_num = max(O_num)                  # 全部工件中工序最多的数值
    for _ in range(len(MS)):
        M_matrix = np.zeros((J_num, max_O_num))         # 工件数，最大工序数
        T_matrix = np.zeros((J_num, max_O_num))
        J_appear = []                       # 记录已经出现过的工件

        for MS_idx, __ in enumerate(OS[_]):
            J_appear.append(__)
            column = J_appear.count(__)         # 获得当前工件出现的次数，即当前工件的工序
            idx = MS[_][MS_idx]
            M_matrix[__ - 1][column - 1] = pro_m[__ - 1][column - 1][idx - 1]
            T_matrix[__ - 1][column - 1] = pro_t[__ - 1][column - 1][idx - 1]
        M_matrix_set.append(M_matrix)                           # 机器顺序矩阵集,第三维形式：[h1,h2,h3]:当前工件的三道工序所选的机器
        T_matrix_set.append(T_matrix)                           # 时间顺序矩阵集，第三维形式：[t1,t2,t3]:三道工序对应的三个时间

    # 对工序排序部分进行解码
    O_jh_set = []  # 工序列表集
    for _ in range(len(OS)):
        O_jh = []  # 存储每个工件的工序
        O_jh_Traverse = []  # 用于记录已经遍历完的工序
        for __ in OS[_]:
            j = __                    # 第j个工件
            O_jh_Traverse.append(__)  # 已经遍历完的工序
            h = O_jh_Traverse.count(j)  # 当前工件的工序(第h道工序)
            O_jh.append([j, h])
        O_jh_set.append(O_jh)           # 工序顺序矩阵集

    #获得工序对应的加工机器和加工时间集
    Pro_Message_set = []  # 加工信息列表集，第三维形式：[j,h,m,t] 第j个工件的第h道工序在机器m上加工，加工时间为t
    for _ in range(len(O_jh_set)):  # 进入第一层
        Pro_Message_2 = []  # 第二维形式：[ [j,h,m,t] , [j,h,m,t]]
        for __ in range(len(O_jh_set[_])):  # 进入O_jh_set第二层
            Pro_Message_3 = []  # 第三维形式：[j,h,m,t]
            for idx, ___ in enumerate(O_jh_set[_][__]):  # 进入O_jh_set第三层
                if idx == 0:
                    O_j = O_jh_set[_][__][idx]
                else:
                    O_h = O_jh_set[_][__][idx]
                Pro_Message_3.append(___)
            Pro_Message_3.append(M_matrix_set[_][O_j - 1][O_h - 1])
            Pro_Message_3.append(T_matrix_set[_][O_j - 1][O_h - 1])
            Pro_Message_2.append(Pro_Message_3)
        Pro_Message_set.append(Pro_Message_2)

    return Pro_Message_set

def Single_Decode(single_ms, single_os):
    """
    单条染色体解码
    :param single_ms: 单条ms染色体，形式如：[2, 1, 2, 3, 2]
    :param single_os: 单条os染色体，形式如：[2, 2, 1, 2, 1]
    :return: 单条染色体的加工数据表(二维)：Pro_Message，形式如：
            [[2, 1, 3.0, 6.0], [2, 2, 2.0, 6.0], [1, 1, 4.0, 3.0], [1, 2, 2.0, 8.0], [2, 3, 5.0, 8.0], ····]
    """
    pro_m, pro_t, J_num, machine_num = Pro_Data()
    #对机器选择部分进行解码
    J_num = len(pro_t)                      # 工件个数
    O_num = []
    for i in range(len(pro_t)):
        O_num.append(len(pro_t[i]))         # 存储每个工件的工序数
    max_O_num = max(O_num)                  # 全部工件中工序最多的数值

    M_matrix = np.zeros((J_num, max_O_num)) # 工件数为2，最大工序数为3
    T_matrix = np.zeros((J_num, max_O_num))
    J_appear = []                           # 记录已经出现过的工件

    for MS_idx, _ in enumerate(single_os):
        J_appear.append(_)
        column = J_appear.count(_)          # 获得当前工件出现的次数，即当前工件的工序
        idx = single_ms[MS_idx]
        M_matrix[_ - 1][column - 1] = pro_m[_ - 1][column - 1][idx - 1]
        T_matrix[_ - 1][column - 1] = pro_t[_ - 1][column - 1][idx - 1]

    #对工序排序部分进行解码
    O_jh = []           # 存储每个工件的工序
    O_jh_Traverse = []  # 用于记录已经遍历完的工序
    for _ in single_os:
        j = _                       # 第j个工件
        O_jh_Traverse.append(_)     # 已经遍历完的工序
        h = O_jh_Traverse.count(j)  # 当前工件的工序(第h道工序)
        O_jh.append([j, h])         # O_jh形式如：[[2, 1], [2, 2], [1, 1], [1, 2], [2, 3], ····]

    #获得工序对应的加工机器和加工时间列表
    Pro_Message= []             # 加工信息列表集，第二维形式：[j,h,m,t] 第j个工件的第h道工序在机器m上加工，加工时间为t
    for _ in range(len(O_jh)):  # 进入O_jh第一层
        Pro_Message_1 = []      # 第二维形式：[j,h,m,t]
        for idx, __ in enumerate(O_jh[_]):  # 进入O_jh第二层
            if idx == 0:
                O_j = O_jh[_][idx]
            else:
                O_h = O_jh[_][idx]
            Pro_Message_1.append(__)
        Pro_Message_1.append(M_matrix[O_j - 1][O_h - 1])
        Pro_Message_1.append(T_matrix[O_j - 1][O_h - 1])
        Pro_Message.append(Pro_Message_1)

    return Pro_Message

#调度方案
def Dispatch(Pro_Message_set):
    """
    调度方案
    调度分为四种情况：①工件出现过，机器也出现过；②工件没有出现过，机器出现过；
                   ③工件出现过，机器没有出现过；④工件没有出现过，机器也没有出现过。

    S_dispatch_list:单工序调度列表，形式如[j,h,m,ts,te]
    j为工件，h为工序，m为加工机器，ts为开始时间，te为结束时间。
    T_dispatch_list: 单群体全工序调度列表，形式如[[j,h,m,ts,te],[j,h,m,ts,te]······]
    P_dispatch_set: 多群体全工序调度集，形式如[[[j,h,m,ts,te],[j,h,m,ts,te]],[[j,h,m,ts,te],[j,h,m,ts,te]]······]
    mts为机器开始加工时间，mte为机器结束时间
    ts为间隔开始时间，te为间隔结束时间

    :param Pro_Message_set: 加工数据集
    :return: 多群体全工序调度集： P_dispatch_set
    """
    # S_dispatch_list = []
    # T_dispatch_list = []
    P_dispatch_set = []
    for i in range(len(Pro_Message_set)):
        for j in range(len(Pro_Message_set[i])):
            J = Pro_Message_set[i][j][0]    #当前工件
            M = Pro_Message_set[i][j][2]    #当前工件所需要的机器
            if j == 0:          #该工件的本次工序为整个流程的第一道工序
                T_dispatch_list = []
                mts = 0; mte = mts + Pro_Message_set[i][j][3]  #开始时间--结束时间
                S_dispatch_list = [Pro_Message_set[i][j][0],Pro_Message_set[i][j][1],
                                   Pro_Message_set[i][j][2],mts,mte]
                T_dispatch_list.append(S_dispatch_list)
            if j != 0:
                J_appear = []  # 记录遍历过的工件，形式如[2,2,1,1,2]
                M_appear = []  # 记录出现过的机器，形式如[1,2,2,3,5,4,5····]
                for k in range(len(T_dispatch_list)):
                    J_appear.append(T_dispatch_list[k][0])
                    M_appear.append(T_dispatch_list[k][2])

                if J not in J_appear:       #-------如果该工件没有出现过(即本次第一次出现)
                    if M not in M_appear:   #-------如果该机器没有出现过
                        mts = 0; mte = mts + Pro_Message_set[i][j][3]
                        S_dispatch_list = [Pro_Message_set[i][j][0], Pro_Message_set[i][j][1],
                                           Pro_Message_set[i][j][2], mts, mte]
                        T_dispatch_list.append(S_dispatch_list)
                    else:               #-------如果该机器出现过(先找到所有间隔时间，接下来就是找到间隔时间进行插入操作)
                        # M_stime_list = []  #记录当前工序需要的机器在过往单个工序的加工开始时间和结束时间，形式如[mts，mte]
                        M_ttime_list = []  # 记录当前工序需要的机器在过往所有工序的加工开始时间和结束时间，形式如[[mts，mte],[mts，mte]····]
                        for _ in range(len(T_dispatch_list)):
                            if M == T_dispatch_list[_][2]:  # 将该机器的所有工序开始时间和结束时间存起来
                                M_stime_list = [T_dispatch_list[_][3], T_dispatch_list[_][4]]
                                M_ttime_list.append(M_stime_list)

                        M_ttime_list.sort()
                        # I_stime_list = []     #某个机器的单个间隔时间列表，形式如[ts,te]
                        I_ttime_list = []       #某个机器的全部间隔开始时间--结束时间列表,形式如[[ts,te],[ts,te]····]
                        # I_time = []           #某个机器的全部间隔时间列表，形式如[2,3,5,1····]
                        for _ in range(len(M_ttime_list)):
                            if _ == 0:
                                interval_time = M_ttime_list[_][0] - 0  # 该机器加工的首道工序的开始时间减去零时刻
                                if interval_time != 0:  # 如果该机器加工时间不是从零时刻开始的
                                    ts = 0; te = M_ttime_list[_][0]
                                    I_stime_list = [ts, te]
                                    I_ttime_list.append(I_stime_list)
                                    # I_time.append(interval_time)
                            if _ != 0:
                                interval_time = M_ttime_list[_][0] - M_ttime_list[_ - 1][1]
                                if interval_time != 0:
                                    ts = M_ttime_list[_ - 1][1]; te = M_ttime_list[_][0]
                                    I_stime_list = [ts, te]
                                    I_ttime_list.append(I_stime_list)
                                    # I_time.append(interval_time)

                        # 开始进行插入操作
                        insert_flag = False  # 插入是否成功的标识
                        for _ in range(len(I_ttime_list)):  # 遍历所有间隔,查找符合插入条件的间隔
                            ts = I_ttime_list[_][0]  # t_s = TS_i;因为是工件的第一道工序，所以工序最早开始加工时间就是间隔开始时间
                            if (ts + Pro_Message_set[i][j][3]) <= I_ttime_list[_][1]:  # t_s + p_ijh <= TE_i;间隔时间充足,可插入
                                mts = ts; mte = mts + Pro_Message_set[i][j][3]
                                S_dispatch_list = [Pro_Message_set[i][j][0], Pro_Message_set[i][j][1],
                                                   Pro_Message_set[i][j][2], mts, mte]
                                T_dispatch_list.append(S_dispatch_list)
                                insert_flag = True  # 插入成功
                                break               # 插入成功之后就必须跳出循环，否则插入成功后还会继续寻找间隔时间做又一次插入操作

                        if insert_flag == False:  # 所有间隔都不满足插入条件,那就插到当前机器最后一道工序的结束时间
                            # M_reversed_idx = M_appear[::-1].index(M)
                            # M_last_idx = len(M_appear) - M_reversed_idx - 1  # 获得当前机器最后一次出现的索引
                            mts = M_ttime_list[len(M_ttime_list) - 1][1]; mte = mts + Pro_Message_set[i][j][3]
                            S_dispatch_list = [Pro_Message_set[i][j][0], Pro_Message_set[i][j][1],
                                               Pro_Message_set[i][j][2], mts, mte]
                            T_dispatch_list.append(S_dispatch_list)

                else:                       #-------如果该工件出现过
                    if M not in M_appear:       #-------如果该机器没有出现过
                        J_reversed_idx = J_appear[::-1].index(J)
                        J_last_idx = len(J_appear) - J_reversed_idx - 1    #获得当前工件最后一次出现的索引
                        mts = T_dispatch_list[J_last_idx][4]; mte = mts + Pro_Message_set[i][j][3] #开始加工时间即为该工件上一道工序的结束时间
                        S_dispatch_list = [Pro_Message_set[i][j][0], Pro_Message_set[i][j][1],
                                           Pro_Message_set[i][j][2], mts, mte]
                        T_dispatch_list.append(S_dispatch_list)
                    else:                   #-------如果该机器出现过(先找到所有间隔时间，接下来就是找到间隔时间进行插入操作)
                        # M_stime_list = []  #记录当前工序需要的机器在过往单个工序的加工开始时间和结束时间，形式如[mts，mte]
                        M_ttime_list = []    #记录当前工序需要的机器在过往所有工序的加工开始时间和结束时间，形式如[[mts，mte],[mts，mte]····]
                        for _ in range(len(T_dispatch_list)):
                            if M == T_dispatch_list[_][2]:      #将该机器的所有工序开始时间和结束时间存起来
                                M_stime_list = [T_dispatch_list[_][3], T_dispatch_list[_][4]]
                                M_ttime_list.append(M_stime_list)

                        M_ttime_list.sort()
                        # I_stime_list = []     #某个机器的单个间隔时间列表，形式如[ts,te]
                        I_ttime_list = []       #某个机器的全部间隔开始时间--结束时间列表,形式如[[ts,te],[ts,te]····]
                        # I_time = []             #某个机器的全部间隔时间列表，形式如[2,3,5,1····]
                        for _ in range(len(M_ttime_list)):
                            if _ == 0:
                                interval_time = M_ttime_list[_][0] - 0  #该机器加工的首道工序的开始时间减去零时刻
                                if interval_time != 0:                  #如果该机器加工时间不是从零时刻开始的
                                    ts = 0; te = M_ttime_list[_][0]
                                    I_stime_list = [ts, te]
                                    I_ttime_list.append(I_stime_list)
                                    # I_time.append(interval_time)
                            if _ != 0:
                                interval_time = M_ttime_list[_][0] - M_ttime_list[_ - 1][1]
                                if interval_time != 0:
                                    ts = M_ttime_list[_ - 1][1]; te = M_ttime_list[_][0]
                                    I_stime_list = [ts, te]
                                    I_ttime_list.append(I_stime_list)
                                    # I_time.append(interval_time)

                        #开始进行插入操作
                        J_reversed_idx = J_appear[::-1].index(J)
                        J_last_idx = len(J_appear) - J_reversed_idx -1    #获得当前工件最后一次出现的索引
                        C_jh_1 = T_dispatch_list[J_last_idx][4]         #该工件上一道工序的结束时间
                        insert_flag = False                             #插入是否成功的标识
                        for _ in range(len(I_ttime_list)):              #遍历所有间隔,查找符合插入条件的间隔
                            ts = max(C_jh_1, I_ttime_list[_][0])                         #t_s = max{C_j(h-1),TS_i};得到工序最早开始加工时间
                            if ( ts + Pro_Message_set[i][j][3] ) <= I_ttime_list[_][1]:  #t_s + p_ijh <= TE_i;间隔时间充足,可插入
                                mts = ts; mte = mts + Pro_Message_set[i][j][3]
                                S_dispatch_list = [Pro_Message_set[i][j][0], Pro_Message_set[i][j][1],
                                                   Pro_Message_set[i][j][2], mts, mte]
                                T_dispatch_list.append(S_dispatch_list)
                                insert_flag = True                      #插入成功
                                break

                        if insert_flag == False:                        #所有间隔都不满足插入条件,那就比较当前机器最后一道工序的结束时间和该工件上一道工序的结束时间
                            # reversed_idx = M_appear[::-1].index(M)
                            # M_last_idx = len(M_appear) - reversed_idx - 1                #获得当前机器最后一次出现的索引
                            mts = max(C_jh_1,M_ttime_list[len(M_ttime_list) - 1][1]); mte = mts + Pro_Message_set[i][j][3]
                            S_dispatch_list = [Pro_Message_set[i][j][0], Pro_Message_set[i][j][1],
                                               Pro_Message_set[i][j][2], mts, mte]
                            T_dispatch_list.append(S_dispatch_list)
        P_dispatch_set.append(T_dispatch_list)

    return P_dispatch_set

# 种群适应度
def Fitness(P_dispatch_set):
    """
    各个种群的调度方案生成后，计算各个种群的适应度(本程序以最小完工时间作为适应度)
    :param P_dispatch_set: 多群体全工序调度集，形式如[[[j,h,m,ts,te],[j,h,m,ts,te]],[[j,h,m,ts,te],[j,h,m,ts,te]]······]
    :return: 各种群适应度(完工时间)：Fitness_list，形式如[22.0, 19.0, 25.0, 12.0, 30.0, 21.0，···]
    """
    Fitness_list = []          #记录所有种群的适应度列表
    for _ in range(len(P_dispatch_set)):
        SFin_time_list = []  # 单个工序完成的时间
        for __ in range(len(P_dispatch_set[_])):
            SFin_time_list.append(P_dispatch_set[_][__][4])
        max_time = max(SFin_time_list)
        Fitness_list.append(max_time)

    return Fitness_list

# if __name__ == "__main__":
    # 测试调度程序逻辑是否正确
    # Pro_Message_set = [[[6, 1, 6.0, 2.0], [6, 2, 1.0, 2.0], [7, 1, 6.0, 1.0], [7, 2, 4.0, 2.0], [8, 1, 6.0, 2.0],
    # [8, 2, 3.0, 4.0], [6, 3, 3.0, 4.0], [5, 1, 2.0, 1.0], [8, 3, 1.0, 1.0], [6, 4, 2.0, 6.0], [9, 1, 6.0, 1.0],
    # [2, 1, 2.0, 6.0], [5, 2, 1.0, 1.0], [8, 4, 2.0, 6.0], [9, 2, 1.0, 1.0], [5, 3, 2.0, 6.0], [4, 1, 1.0, 1.0],
    # [8, 5, 2.0, 6.0], [4, 2, 2.0, 6.0], [5, 4, 3.0, 4.0], [9, 3, 4.0, 3.0], [3, 1, 2.0, 6.0], [4, 3, 3.0, 1.0],
    # [7, 3, 3.0, 4.0], [1, 1, 3.0, 4.0], [9, 4, 1.0, 2.0], [10, 1, 6.0, 2.0], [2, 2, 3.0, 1.0], [4, 4, 2.0, 1.0],
    # [10, 2, 3.0, 4.0], [1, 2, 2.0, 1.0], [10, 3, 2.0, 1.0], [2, 3, 1.0, 2.0], [3, 2, 6.0, 2.0], [9, 5, 3.0, 4.0],
    # [6, 5, 1.0, 1.0], [1, 3, 6.0, 2.0], [3, 3, 1.0, 1.0], [5, 5, 4.0, 6.0], [7, 4, 5.0, 1.0], [3, 4, 3.0, 4.0],
    # [3, 5, 1.0, 1.0], [1, 4, 1.0, 1.0], [10, 4, 6.0, 1.0], [7, 5, 3.0, 1.0], [1, 5, 3.0, 1.0], [9, 6, 2.0, 6.0],
    # [5, 6, 3.0, 4.0], [6, 6, 4.0, 2.0], [10, 5, 2.0, 6.0], [1, 6, 4.0, 3.0], [2, 4, 2.0, 6.0], [2, 5, 1.0, 1.0],
    # [4, 5, 6.0, 2.0], [10, 6, 4.0, 2.0]]]
    # Pro_Message_set = [[[1, 1, 1.0, 5.0], [1, 2, 2.0, 1.0], [10, 1, 6.0, 2.0], [5, 1, 2.0, 1.0], [2, 1, 2.0, 6.0], [1, 3, 6.0, 2.0],
    #  [7, 1, 6.0, 1.0], [2, 2, 3.0, 1.0], [9, 1, 6.0, 1.0], [6, 1, 6.0, 2.0], [8, 1, 6.0, 2.0], [9, 2, 1.0, 1.0],
    #  [7, 2, 4.0, 2.0], [6, 2, 1.0, 2.0], [5, 2, 1.0, 1.0], [7, 3, 3.0, 4.0], [9, 3, 4.0, 3.0], [7, 4, 5.0, 1.0],
    #  [10, 2, 3.0, 4.0], [4, 1, 1.0, 1.0], [8, 2, 3.0, 4.0], [9, 4, 1.0, 2.0], [4, 2, 2.0, 6.0], [10, 3, 2.0, 1.0],
    #  [3, 1, 2.0, 6.0], [4, 3, 3.0, 1.0], [3, 2, 6.0, 2.0], [2, 3, 1.0, 2.0], [5, 3, 2.0, 6.0], [5, 4, 3.0, 4.0],
    #  [9, 5, 3.0, 4.0], [10, 4, 6.0, 1.0], [5, 5, 2.0, 6.0], [8, 3, 1.0, 1.0], [3, 3, 1.0, 1.0], [1, 4, 1.0, 1.0],
    #  [4, 4, 2.0, 1.0], [10, 5, 4.0, 6.0], [4, 5, 6.0, 2.0], [8, 4, 2.0, 6.0], [3, 4, 3.0, 4.0], [10, 6, 4.0, 2.0],
    #  [3, 5, 1.0, 1.0], [6, 3, 3.0, 4.0], [1, 5, 3.0, 1.0], [1, 6, 4.0, 3.0], [7, 5, 3.0, 1.0], [6, 4, 2.0, 6.0],
    #  [2, 4, 4.0, 6.0], [5, 6, 3.0, 4.0], [6, 5, 1.0, 1.0], [9, 6, 2.0, 6.0], [8, 5, 4.0, 6.0], [2, 5, 1.0, 1.0],
    #  [6, 6, 4.0, 2.0]]]
    #
    # P_dispatch_set = Dispatch(Pro_Message_set)

    # 使用2工件5工序5机器的数据集测试调度方案是否正确
    # OS = [[2, 1, 2, 1, 2], [2, 1, 2, 1, 2], [1, 1, 2, 2, 2], [2, 2, 1, 2, 1], [1, 2, 2, 1, 2]]
    # MS = [[2, 4, 2, 2, 4], [2, 2, 1, 2, 4], [3, 1, 1, 2, 4], [3, 1, 4, 2, 1], [4, 3, 1, 1, 4]]
    # Pro_Message_set = Decode(MS, OS)
    # print(Pro_Message_set)