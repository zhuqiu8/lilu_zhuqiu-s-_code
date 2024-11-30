
#通过动态规划算法，计算一个堆场里面 对同一品牌 计算其最大的 排放数量
# 目前 这个代码里面没有考虑 每种品牌尺寸的小矩形的数量

# def max_rectangles(W, H, rectangles):
#     """
#     计算在大矩形中能放置的小矩形的最大数量，并返回方案。
    
#     参数：
#         W: int - 大矩形的宽度
#         H: int - 大矩形的高度
#         rectangles: list - 小矩形集合 [(w1, h1), (w2, h2), ...]

#     返回：
#         max_count: int - 能放置的车的最大数量
#         placement: list - 放置方案 [(x, y, w, h)]，每个元组表示一个车的位置和尺寸
#     """
#     # 初始化 DP 表和方案记录
#     dp = [[0] * (H + 1) for _ in range(W + 1)]
#     placement = [[[] for _ in range(H + 1)] for _ in range(W + 1)]
    
#     # 遍历每一个状态
#     for w in range(1, W + 1):
#         for h in range(1, H + 1):
#             # 遍历所有的小矩形
#             for rect in rectangles:
#                 rw, rh = rect  # 小矩形的宽和高
#                 # 不旋转放置
#                 if rw <= w and rh <= h:
#                     new_count = 1 + dp[w - rw][h] + dp[w][h - rh]
#                     if new_count > dp[w][h]:
#                         dp[w][h] = new_count
#                         # 更新方案：当前位置放置 rw x rh 的矩形
#                         placement[w][h] = (
#                             [(0, 0, rw, rh)] +
#                             [(x + rw, y, pw, ph) for x, y, pw, ph in placement[w - rw][h]] +
#                             [(x, y + rh, pw, ph) for x, y, pw, ph in placement[w][h - rh]]
#                         )
#                 # 旋转放置
#                 if rh <= w and rw <= h:
#                     new_count = 1 + dp[w - rh][h] + dp[w][h - rw]
#                     if new_count > dp[w][h]:
#                         dp[w][h] = new_count
#                         # 更新方案：当前位置放置 rh x rw 的矩形（旋转）
#                         placement[w][h] = (
#                             [(0, 0, rh, rw)] +
#                             [(x + rh, y, pw, ph) for x, y, pw, ph in placement[w - rh][h]] +
#                             [(x, y + rw, pw, ph) for x, y, pw, ph in placement[w][h - rw]]
#                         )
    
#     # 返回最大数量和具体方案
#     return dp[W][H], placement[W][H]

# 更改 ，加入不同类型车辆的数量限制

def max_rectangles(W, H, rectangles):
    """
    计算在大矩形中能放置的小矩形的最大数量，并返回方案。
    
    参数：
        W: int - 大矩形的宽度
        H: int - 大矩形的高度
        rectangles: dict - 小矩形集合 { (w1, h1): count1, (w2, h2): count2, ... }

    返回：
        max_count: int - 能放置的车的最大数量
        placement: list - 放置方案 [(x, y, w, h)]，每个元组表示一个车的位置和尺寸
    """

    W =  int(W)
    H = int(H)

    # 初始化 DP 表和方案记录
    dp = [[0] * (H + 1) for _ in range(W + 1)]
    placement = [[[] for _ in range(H + 1)] for _ in range(W + 1)]

    # 遍历每一个状态
    for w in range(1, W + 1):
        for h in range(1, H + 1):
            # 遍历所有的小矩形
            for rect, count in rectangles.items():
                rw, rh = rect  # 小矩形的宽和高
                # 不旋转放置
                if rw <= w and rh <= h and count > 0:
                    new_count = 1 + dp[w - rw][h] + dp[w][h - rh]
                    if new_count > dp[w][h]:
                        # 检查是否能满足数量约束
                        used_count = (
                            sum(1 for x, y, pw, ph in placement[w - rw][h] if (pw, ph) == rect) +
                            sum(1 for x, y, pw, ph in placement[w][h - rh] if (pw, ph) == rect)
                        )
                        if used_count + 1 <= count:
                            dp[w][h] = new_count
                            # 更新方案：当前位置放置 rw x rh 的矩形
                            placement[w][h] = (
                                [(0, 0, rw, rh)] +
                                [(x + rw, y, pw, ph) for x, y, pw, ph in placement[w - rw][h]] +
                                [(x, y + rh, pw, ph) for x, y, pw, ph in placement[w][h - rh]]
                            )
                # 旋转放置
                if rh <= w and rw <= h and count > 0:
                    new_count = 1 + dp[w - rh][h] + dp[w][h - rw]
                    if new_count > dp[w][h]:
                        # 检查是否能满足数量约束
                        used_count = (
                            sum(1 for x, y, pw, ph in placement[w - rh][h] if (ph, pw) == rect) +
                            sum(1 for x, y, pw, ph in placement[w][h - rw] if (ph, pw) == rect)
                        )
                        if used_count + 1 <= count:
                            dp[w][h] = new_count
                            # 更新方案：当前位置放置 rh x rw 的矩形（旋转）
                            placement[w][h] = (
                                [(0, 0, rh, rw)] +
                                [(x + rh, y, pw, ph) for x, y, pw, ph in placement[w - rh][h]] +
                                [(x, y + rw, pw, ph) for x, y, pw, ph in placement[w][h - rw]]
                            )

    # 返回最大数量和具体方案
    return dp[W][H], placement[W][H]
