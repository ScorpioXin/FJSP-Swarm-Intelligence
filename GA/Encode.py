from Pro_Data import Pro_Data

import copy
import random
random.seed(10)

class Encode:
    """
    编码的类：包含OS随机选择编码、MS选择全局编码、局部选择编码和随机选择编码
    """

    # OS随机编码
    def encode_OS(self):
        """
        :return: OS随机编码的列表，形式如[7, 6, 9, 10, 9, ····]
        """
        os_list = [_ + 1 for _ in range(len(pro_t)) for __ in range(len(pro_t[_]))]     # OS段的编码准备
        random.shuffle(os_list)     # 通过打乱os_list获得一个随机OS段
        return os_list

    # MS全局选择编码
    def encode_GMS(self, machine_num):
        """
        :param machine_num: 机器数量
        :return: MS全局选择编码的列表，形式如[1, 1, 2, 3, 1, ····]
        """
        ms_list = []
        ms_info = copy.deepcopy(pro_t)
        for i in range(len(pro_t)):
            for j in range(len(pro_t[i])):
                ms_info[i][j] = [0]      # ms_info存储信息的形式与pro_t是一样的，方便各工件选择机器后的信息存储

        Machine_time_list = [0 for _ in range(machine_num)]
        J_storage = []           # 记录已经遍历过的工件工序
        OS = self.encode_OS()
        random.shuffle(OS)
        seq_list = list(set(OS))
        J_seq = seq_list
        random.shuffle(J_seq)
        OS_random = [_ for _ in J_seq for __ in range(OS.count(_))]
        # OS_random = [2, 2, 2, 1, 1]  # 测试用
        # print(f' OS_random:{OS_random}')

        for _ in range(len(OS_random)):
            time_add = []  # 记录加工时间相加的列表
            J = OS_random.pop(0)
            # J = OS.pop(0)   #测试用

            J_storage.append(J)
            J_cout = J_storage.count(J)  # 记录某工件出现次数，亦即某工件的工序
            for idx, __ in enumerate(pro_t[J - 1][J_cout - 1]):
                machine_idx = pro_m[J - 1][J_cout - 1][idx]
                time_storage = Machine_time_list[machine_idx - 1] + __  # 加工时间相加
                time_add.append(time_storage)

            min_load = min(time_add)  # 最小负荷
            min_idx = time_add.index(min_load)  # 最小负荷机器的索引
            min_machine_idx = pro_m[J - 1][J_cout - 1][min_idx]
            Machine_time_list[min_machine_idx - 1] = min(time_add)  # 更新时间列表
            ms_info[J - 1][J_cout - 1][0] = min_idx + 1

        for i in range(len(ms_info)):
            for j in range(len(ms_info[i])):
                ms_list.append(ms_info[i][j][0])  # 将存储形式转换成[a,b,c·····]

        return ms_list

    # MS局部选择编码
    def encode_LMS(self):
        """
        :return: MS局部选择编码的列表，形式如[2, 3, 2, 3, 1, ····]
        """
        ms_list = []
        Machine_time_list = [0 for _ in range(machine_num)]

        J_storage = []          #记录已经遍历过的工件工序
        OS_random = self.encode_OS()
        OS_random.sort()        #工件顺序序列集，形式如[1,1,2,2,2]

        for _ in range(len(OS_random)):
            time_add = []  # 记录加工时间相加的列表
            J = OS_random.pop(0)    #弹出列表中的首个工序
            J_storage.append(J)
            J_cout = J_storage.count(J)     #记录某工件出现次数，某工件亦即工序
            for idx, __ in enumerate(pro_t[J-1][J_cout-1]):
                machine_idx = pro_m[J-1][J_cout-1][idx]
                time_storage = Machine_time_list[machine_idx-1] + __      #加工时间相加
                time_add.append(time_storage)

            min_load = min(time_add)            #最小负荷
            min_idx = time_add.index(min_load)  #最小负荷机器的索引
            min_machine_idx = pro_m[J-1][J_cout-1][min_idx]
            Machine_time_list[min_machine_idx-1] = min(time_add)     #更新时间列表
            ms_list.append(min_idx + 1)
            if J not in OS_random:   #当前工件的所有工序都已经遍历完
                Machine_time_list = [0 for _ in range(machine_num)]   #时间列表重新置零
        return ms_list

    # MS段随机编码
    def encode_RMS(self):
        """
        :return: MS随机选择编码的列表，形式如[1, 3, 2, 3, 1, ····]
        """
        # MS段编码准备
        Max_M_num = [len(pro_t[_][__]) for _ in range(len(pro_t)) for __ in range(len(pro_t[_]))]
        # 从可选加工机器中随机选择一个
        ms_list = [random.randint(1, _) for _ in Max_M_num]
        return ms_list

Encode = Encode()         #创建类的实例
pro_m, pro_t, J_num, machine_num = Pro_Data()
os_list = Encode.encode_OS()
ms_list = Encode.encode_RMS()

if __name__ == "__main__":
    print("ROS:{}\nRMS:{}".format(os_list, ms_list))
    GMS = Encode.encode_GMS(machine_num)
    print(f'GMS:{GMS}')
    LMS = Encode.encode_LMS()
    print(f'LMS:{LMS}')
    print(f'可选机器列表：{pro_m}')
    print(f'可加工时间列表：{pro_t}')