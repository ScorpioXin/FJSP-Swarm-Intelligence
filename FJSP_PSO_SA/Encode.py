from Pro_Data import Pro_Data

import random


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

    # MS段随机编码
    def encode_MS(self):
        """
        :return: MS随机选择编码的列表，形式如[1, 3, 2, 3, 1, ····]
        """
        # MS段编码准备
        os_list = self.encode_OS()              # 获得OS编码，只有当OS编码完成才能进行MS编码
        Max_M_num = []
        for _ in range(len(os_list)):
            j_appear = os_list[:_+1]
            j_label = j_appear[_]                       # 工件编号
            j_order = j_appear.count(j_appear[_])       # 工序
            Max_M_num.append(len(pro_m[j_label-1][j_order-1]))
        # 从可选加工机器中随机选择一个
        ms_list = [random.randint(1, _) for _ in Max_M_num]
        # print(Max_M_num)
        return ms_list, os_list

#随机生成初始种群
def Init_Pop(Pop_size):
    """
    种群初始化
    :param Pop_size: 种群大小
    :return: MS：机器选择部分；OS：工序排序部分
    """
    OS, MS = [], []
    for _ in range(Pop_size):
        ms_list, os_list= Encode.encode_MS()   # OS,MS种群随机选择
        MS.append(ms_list)
        OS.append(os_list)
    return MS, OS

Encode = Encode()         #创建类的实例
pro_m, pro_t, J_num, machine_num = Pro_Data()
ms_list, os_list = Encode.encode_MS()

if __name__ == "__main__":
    MS, OS = [], []
    for _ in range(5):
        ms_list, os_list = Encode.encode_MS()
        OS.append(os_list)
        MS.append(ms_list)
    print(f"OS = {OS}")
    print(f"MS = {MS}")
    # MS, OS = Encode.encode_MS()
    # print(f'MS:{MS}')
    # print(f'可选机器列表：{pro_m}')
    # print(f'可加工时间列表：{pro_t}')