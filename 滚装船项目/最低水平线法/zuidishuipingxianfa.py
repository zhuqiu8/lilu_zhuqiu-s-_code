import copy
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm


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
    def enhance_line(self, index, max_height=450):
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

            #增加水平线的高度约束，即为堆场的长度约束
            new_height = max(self.line_list[index].height, old.height)

            # 如果超过高度限制，停止提升
            if new_height > max_height:
                print(f"Cannot enhance line at index {index}, height limit reached.")
                return False
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
    #堆场的高度
    max_height = 450  # 根据需求调整
    # 堆场的宽度
    container_width = 32
    # 矩形物品数量
    item_num = 718+327+100
    # 初始化矩形物品尺寸，也可以随机生成
    # item_sizes = [[3, 1], [4, 4], [1, 1], [2, 3], [2, 4], [3, 4], [1, 4], [2, 2], [3, 3], [3, 1], [4, 2], [3, 1],
    #               [3, 1], [3, 2], [4, 2], [1, 2], [1, 3], [3, 4], [2, 3], [1, 1], [2, 1], [3, 2], [4, 3], [3, 2],
    #               [4, 3]]
    item_sizes = [[4.5,2.2]] *  718 +  [[5,2.2]]*327 + [[4.5 , 2.2]] *100




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
            # 如果无法直接放置，尝试提升线。如果无法提升，跳过当前矩形。
            if not layout.enhance_line(lowest_idx, max_height):
                print(f"Skipping product {pro.num}, cannot fit within height limit.")
                _products.pop(0)
                
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
    fig = plt.figure(figsize=(container_width / 5, container_height / 5))
    plt.xlim(0, container_width)
    plt.ylim(0, container_height)
    plt.axis("off")
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(0, container_width)
    ax.set_ylim(0, container_height)

    # 使用颜色映射
    cmap = cm.get_cmap('tab20', len(result_pos))
    for idx, pos in enumerate(result_pos):
        pro = Product.by_num(pos[0], products)
        ax.add_patch(
            plt.Rectangle(
                (pos[1], pos[2]),
                pro.w,
                pro.h,
                color=cmap(idx),
                alpha=0.7,  # 半透明
                edgecolor='black',
                linewidth=0.5
            )
        )
        # 显示部分编号
        if pos[0] % 100 == 0:  # 每隔 100 个矩形显示一个编号
            ax.text(pos[1] + pro.w / 2, pos[2] + pro.h / 2, "{}".format(pos[0]), fontsize=5, ha='center')


    plt.savefig('./lowest_horizontal_line.png', dpi=900)


