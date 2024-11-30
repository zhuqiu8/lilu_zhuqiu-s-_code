import random

def genetic_algorithm_max_rectangles(W, H, rectangles, max_generations=100, population_size=50, mutation_rate=0.1):
    """
    遗传算法求解二维矩形装箱问题

    参数：
        W: int - 大矩形的宽度
        H: int - 大矩形的高度
        rectangles: dict - 小矩形集合 { (w1, h1): count1, (w2, h2): count2, ... }
        max_generations: int - 最大代数
        population_size: int - 种群规模
        mutation_rate: float - 变异率

    返回：
        best_solution: list - 最佳放置方案 [(x, y, w, h)]
        best_fitness: int - 对应的最大矩形数量
    """
    def create_individual():
        """随机生成个体"""
        individual = []
        for (rw, rh), count in rectangles.items():
            for _ in range(count):
                x = random.randint(0, W - rw)
                y = random.randint(0, H - rh)
                individual.append((x, y, rw, rh))
        random.shuffle(individual)
        return individual

    def fitness(individual):
        """计算适应度（放置的矩形数量）"""
        placed = []
        for rect in individual:
            if not is_overlapping(rect, placed) and is_within_bounds(rect):
                placed.append(rect)
        return len(placed), placed

    def is_overlapping(new_rect, placed_rects):
        """检查是否重叠"""
        nx, ny, nw, nh = new_rect
        for x, y, w, h in placed_rects:
            if not (nx + nw <= x or nx >= x + w or ny + nh <= y or ny >= y + h):
                return True
        return False

    def is_within_bounds(rect):
        """检查是否在边界内"""
        x, y, w, h = rect
        return 0 <= x <= W - w and 0 <= y <= H - h

    def crossover(parent1, parent2):
        """交叉操作"""
        cut = random.randint(0, len(parent1) - 1)
        child1 = parent1[:cut] + parent2[cut:]
        child2 = parent2[:cut] + parent1[cut:]
        return child1, child2

    def mutate(individual):
        """变异操作"""
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                x = random.randint(0, W - individual[i][2])
                y = random.randint(0, H - individual[i][3])
                individual[i] = (x, y, individual[i][2], individual[i][3])
        return individual

    # 初始化种群
    population = [create_individual() for _ in range(population_size)]

    best_solution = None
    best_fitness = 0

    # 遗传算法迭代
    for generation in range(max_generations):
        # 计算适应度
        fitness_scores = [fitness(ind) for ind in population]
        fitness_values = [score[0] for score in fitness_scores]

        # 更新最佳解
        max_fit_idx = fitness_values.index(max(fitness_values))
        if fitness_values[max_fit_idx] > best_fitness:
            best_fitness = fitness_values[max_fit_idx]
            best_solution = fitness_scores[max_fit_idx][1]

        # 选择操作
        selected = random.choices(
            population,
            weights=fitness_values,
            k=population_size
        )

        # 交叉操作
        next_generation = []
        for i in range(0, population_size, 2):
            parent1, parent2 = selected[i], selected[(i + 1) % population_size]
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(child1)
            next_generation.append(child2)

        # 变异操作
        population = [mutate(ind) for ind in next_generation]

    return best_solution, best_fitness
