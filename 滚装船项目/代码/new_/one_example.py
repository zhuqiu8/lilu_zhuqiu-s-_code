from genetic_algorithm_max_area import genetic_algorithm_max_area
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_solution(W, H, solution):
    """可视化矩形布局"""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect('equal')
    ax.set_title("Rectangles Placement")
    ax.set_xlabel("Width")
    ax.set_ylabel("Height")

    # 画矩形
    for x, y, w, h in solution:
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='blue', facecolor='cyan', alpha=0.6)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, f"{w}x{h}", ha='center', va='center', fontsize=8)

    # 画边界
    border = patches.Rectangle((0, 0), W, H, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(border)
    plt.show()

# 示例运行

W, H = 4, 6
rectangles = {
    (2, 3): 5,  # 2x3 矩形最多放置 5 个
    (3, 2): 3,  # 3x2 矩形最多放置 3 个
    (1, 1): 10  # 1x1 矩形最多放置 10 个
}
solution, max_utilization = genetic_algorithm_max_area(W, H, rectangles)
print("最大面积利用率:", max_utilization)
print("放置方案:", solution)

# 可视化方案
visualize_solution(W, H, solution)
