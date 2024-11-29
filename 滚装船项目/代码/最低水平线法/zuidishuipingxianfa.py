
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



