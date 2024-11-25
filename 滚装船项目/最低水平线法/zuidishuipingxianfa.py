import copy
import matplotlib.pyplot as plt
import numpy as np


# 水平线类（起始x位置，终止x位置，高度）
class OutLine:
    def __init__(self, origin, end, height):
        self.origin = origin
        self.end = end
        self.height = height

    def __str__(self):
        return "OutLine:origin:{}, end:{}, height:{}".format(self.origin, self.end, self.height)


# 矩形物品类（宽度，高度，编号）
class Product:
    def __init__(self, w, h, num=0):
        self.w = w
        self.h = h
        self.num = num

    def __str__(self):
        return "product:w:{}, h:{}, num:{}".format(self.w, self.h, self.num)

    @staticmethod
    def by_num(num, data):
        _l = [d for d in data if d.num == num]
        return _l[0] if len(_l) > 0 else None


# 布局类
class RectLayout:
    def __init__(self, line_list=[]):
        self.line_list = line_list

    # 初始化水平线集合（起始x位置，终止x位置，高度）
    def init_line_list(self, origin, end, height):
        self.line_list.append(OutLine(origin, end, height))

    # 提升最低水平线
    def enhance_line(self, index):
        if len(self.line_list) > 1:
            # 获取高度较低的相邻水平线索引，并更新水平线集
            neighbor_idx = 0
            if index == 0:
                neighbor_idx = 1
            elif index + 1 == len(self.line_list):
                neighbor_idx = index - 1
            else:
                # 左边相邻水平线
                left_neighbor = self.line_list[index - 1]
                # 右边相邻水平线
                right_neighbor = self.line_list[index + 1]
                # 选择高度较低的相邻水平线，左右相邻水平线高度相同时，选择左边相邻的水平线
                if left_neighbor.height < right_neighbor.height:
                    neighbor_idx = index - 1
                elif left_neighbor.height == right_neighbor.height:
                    if left_neighbor.origin < right_neighbor.origin:
                        neighbor_idx = index - 1
                    else:
                        neighbor_idx = index + 1
                else:
                    neighbor_idx = index + 1
            # 选中的高度较低的相邻水平线
            old = self.line_list[neighbor_idx]
            # 更新相邻水平线
            if neighbor_idx < index:
                self.line_list[neighbor_idx] = OutLine(old.origin, old.end + self.line_width(index), old.height)
            else:
                self.line_list[neighbor_idx] = OutLine(old.origin - self.line_width(index), old.end, old.height)
            # 删除当前水平线
            del self.line_list[index]

    # 按位置更新水平线
    def update_line_list(self, index, new_line):
        self.line_list[index] = new_line

    # 按位置插入水平线（插在某索引位置后面）
    def insert_line_list(self, index, new_line):
        new_lists = []
        if len(self.line_list) == index + 1:
            new_lists = self.line_list + [new_line]
        else:
            new_lists = self.line_list[:index + 1] + [new_line] + self.line_list[index + 1:]
        self.line_list = new_lists

    # 计算水平线宽度
    def line_width(self, index):
        line = self.line_list[index]
        return line.end - line.origin

    # 找出最低水平线（如果最低水平线不止一条则选取最左边的那条）
    def find_lowest_line(self):
        # 最低高度
        lowest = min([_l.height for _l in self.line_list])
        # 最低高度时，最小开始横坐标
        origin = min([_l.origin for _l in self.line_list if _l.height == lowest])
        for _idx, _line in enumerate(self.line_list):
            if _line.height == lowest and _line.origin == origin:
                return _line, _idx
        return None, None

    # 清空水平线集合
    def empty_line_list(self):
        self.line_list.clear()

    # 计算最高水平线高度，即所用板材最大高度
    def cal_high_line(self):
        max_height = max([ll.height for ll in self.line_list])
        return max_height


# 主方法
if __name__ == "__main__":
    # 板材宽度
    container_width = 10
    # 矩形物品数量
    item_num = 25
    # 初始化矩形物品尺寸，也可以随机生成
    # item_sizes = np.random.randint(1, 8, size=(item_num, 2)).tolist()
    item_sizes = [[3, 1], [4, 4], [1, 1], [2, 3], [2, 4], [3, 4], [1, 4], [2, 2], [3, 3], [3, 1], [4, 2], [3, 1],
                  [3, 1], [3, 2], [4, 2], [1, 2], [1, 3], [3, 4], [2, 3], [1, 1], [2, 1], [3, 2], [4, 3], [3, 2],
                  [4, 3]]
    # 按面积对矩形物品尺寸排序
    _item_sizes = sorted(item_sizes, key=lambda x: x[0] * x[1], reverse=True)
    print(_item_sizes)
    # 排样序号
    ran = [i + 1 for i in range(item_num)]
    print(ran)
    # 矩形物品列表
    products = []
    for idx in range(item_num):
        products.append(Product(_item_sizes[idx][0], _item_sizes[idx][1], ran[idx]))
    # 初始化布局类
    layout = RectLayout()
    # 初始化水平线集
    layout.init_line_list(0, container_width, 0)
    # 最终位置结果[[矩形件编号,左下角横坐标,左下角纵坐标], ...]
    result_pos = []
    _products = copy.deepcopy(products)
    while _products:
        # 取出首部矩形件
        pro = _products[0]
        # 最低水平线及其索引
        lowest_line, lowest_idx = layout.find_lowest_line()
        # 可用长度
        available_width = layout.line_width(lowest_idx)
        if lowest_line is None and lowest_idx is None:
            exit(0)
        if available_width >= pro.w:
            # 对矩形件排样
            result_pos.append([pro.num, lowest_line.origin, lowest_line.height])
            # 更新水平线集
            new_line1 = OutLine(lowest_line.origin, lowest_line.origin + pro.w, lowest_line.height + pro.h)
            new_line2 = OutLine(lowest_line.origin + pro.w, lowest_line.origin + available_width, lowest_line.height)
            layout.update_line_list(lowest_idx, new_line1)
            if available_width - pro.w > 0:
                layout.insert_line_list(lowest_idx, new_line2)
            # 剔除已经排样的物品
            _products.pop(0)
        else:
            # 最低水平线宽度小于要排样矩形宽度，提升最低水平线
            layout.enhance_line(lowest_idx)
    # 计算最大排样高度
    container_height = layout.cal_high_line()
    # 计算板材利用率
    used_area = 0
    for pos in result_pos:
        _p = Product.by_num(pos[0], products)
        used_area += _p.w * _p.h
    print("used_area: {}".format(used_area))
    print("ratio: {}%".format(round((used_area * 100) / (container_width * container_height), 3)))

    # 绘制排样布局
    fig = plt.figure()
    plt.xlim(0, container_width)
    plt.ylim(0, container_height)
    plt.axis("off")
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(0, container_width)
    ax.set_ylim(0, container_height)

    for pos in result_pos:
        pro = Product.by_num(pos[0], products)
        ax.add_patch(
            plt.Rectangle(
                (pos[1], pos[2]),  # 矩形左下角
                pro.w,  # 长
                pro.h,  # 宽
                alpha=1,
                edgecolor='black',
                linewidth=1
            )
        )
        # 物品编号
        ax.text(pos[1] + pro.w / 2, pos[2] + pro.h / 2, "{}".format(pos[0]), transform=ax.transData)

    # plt.show()
    plt.savefig('lowest_horizontal_line.png', dpi=800)

