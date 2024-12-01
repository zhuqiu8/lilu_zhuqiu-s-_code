import numpy as np
import random

# 多个矩形面
containers = [{"id": 1, "width": 100, "height": 100}, 
              {"id": 2, "width": 80, "height": 120}]

# 玩具数据
toys = [
    {"id": 1, "brand": "A", "width": 10, "height": 15},
    {"id": 2, "brand": "A", "width": 10, "height": 15},
    {"id": 3, "brand": "B", "width": 20, "height": 10},
    {"id": 4, "brand": "B", "width": 20, "height": 10},
    {"id": 5, "brand": "C", "width": 15, "height": 15},
    # ... 添加更多玩具
]

# 初始化分配
def initialize_allocation(toys, containers):
    allocation = []
    for toy in toys:
        container_id = random.choice(range(len(containers)))
        allocation.append(container_id)
    return allocation

# 品牌分散惩罚
def brand_penalty(allocation, toys, containers):
    brands = set(toy["brand"] for toy in toys)
    penalty = 0
    for brand in brands:
        # 找到该品牌的所有玩具
        brand_toys = [i for i, toy in enumerate(toys) if toy["brand"] == brand]
        # 计算该品牌的矩形面分布
        used_containers = set(allocation[i] for i in brand_toys)
        # 惩罚分布在多个矩形面的情况
        penalty += len(used_containers) - 1
    return penalty

# 目标函数
def objective_with_brand_priority(allocation, positions, toys, containers, lambda_brand=10):
    # 计算品牌分散惩罚
    brand_pen = brand_penalty(allocation, toys, containers)
    # 添加品牌优先策略到目标函数
    return lambda_brand * brand_pen

# 模拟退火框架
def simulated_annealing_with_brand_priority(toys, containers, max_iter=1000):
    allocation = initialize_allocation(toys, containers)
    best_allocation = allocation[:]
    best_penalty = objective_with_brand_priority(allocation, [], toys, containers)

    for t in range(max_iter):
        # 随机调整分配
        new_allocation = allocation[:]
        i = random.randint(0, len(toys) - 1)
        new_allocation[i] = random.choice(range(len(containers)))
        
        # 计算新分配的惩罚
        new_penalty = objective_with_brand_priority(new_allocation, [], toys, containers)
        
        # 接受新分配
        if new_penalty < best_penalty or random.random() < np.exp((best_penalty - new_penalty) / (1 + t)):
            allocation = new_allocation
            best_penalty = new_penalty
            best_allocation = allocation[:]

    return best_allocation, best_penalty

# 运行
allocation, penalty = simulated_annealing_with_brand_priority(toys, containers)
print("最终分配：", allocation)
print("目标函数值（品牌分散惩罚）：", penalty)
