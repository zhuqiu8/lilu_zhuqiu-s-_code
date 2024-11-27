import numpy as np


item_num = 718 + 327 + 100   #车的数量
item_sizes = [[4.5, 2.2]] * 718 + [[5, 2.2]] * 327 + [[4.5, 2.2]] * 100  #车的面积大小


#做一个所有堆场长宽的集合，然后做循环迭代每一个堆场
container= {'ca1':  np.array([9.2,  200]),   #1区的第一个小方块
            'ca2':  np.array([34, 150]),     #1区的第二个小方块
            'ca3':  np.array([52, 135]),
            'ca4':  np.array([9.6, 150]),
            'ca5':  np.array([18, 100]),
            'c2':  np.array([14.5, 270]),
            'c3':  np.array([34, 270]),
            'c4':  np.array([34, 100]),
            'c5':   np.array([14.5, 250]),
            'c6':   np.array([34, 35]),
            # 'c10':  np.array([]),
            'c9':   np.array([32, 450]),      #9区
            # 'c10':  np.array([]),           10区 不规则图形
            # 'c11':  np.array([14,  200]),   11区暂存区
            }


# 定义获取堆场限制的函数
def container_xianzhi(key):  # 堆场 高宽限制
    if key in container:
        value1, value2 = container[key]
        return value1, value2  # 返回堆场的 宽度 和 高度限制
    else:
        raise KeyError(f"Key '{key}' 不能在堆场集合中找到.")