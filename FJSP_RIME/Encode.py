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
        Max_M_num = [len(pro_t[_][__]) for _ in range(len(pro_t)) for __ in range(len(pro_t[_]))]
        # 从可选加工机器中随机选择一个
        ms_list = [random.randint(1, _) for _ in Max_M_num]
        return ms_list

#随机生成初始种群
def Init_Pop(Pop_size):
    """
    种群初始化
    :param Pop_size: 种群大小
    :return: MS：机器选择部分；OS：工序排序部分
    """
    OS, MS = [], []
    for _ in range(Pop_size):     #确保OS与MS的染色体组数相同，这样才能一一对应
        os_list = Encode.encode_OS()   #OS种群全部随机选择
        OS.append(os_list)
        ms_list = Encode.encode_MS()  #MS随机选择部分
        MS.append(ms_list)
    return MS, OS

Encode = Encode()         #创建类的实例
pro_m, pro_t, J_num, machine_num = Pro_Data()
os_list = Encode.encode_OS()

# if __name__ == "__main__":
#     MS, OS = Init_Pop(10)
#     print(MS)
#     print(OS)