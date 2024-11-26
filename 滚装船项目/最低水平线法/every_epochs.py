# 主方法
import copy
import matplotlib.pyplot as plt
from matplotlib import cm
from zuidishuipingxianfa import __init__
from zuidishuipingxianfa import Product
from zuidishuipingxianfa import RectLayout
from zuidishuipingxianfa import OutLine
from item import item_num , item_sizes, max_height, container_width


def layout_items(item_sizes, item_num, container_width, max_height):


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
    utilization = round((used_area * 100) / (container_width * container_height), 3)
    print("占用的面积: {}".format(used_area))
    print("堆场利用率: {}%".format(utilization))

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

     # 保存图片
    output_file = './lowest_horizontal_line.png'
    plt.savefig(output_file, dpi=900)

    return container_height, utilization, output_file