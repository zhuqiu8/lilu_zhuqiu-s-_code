import random

def genetic_algorithm_max_area(W, H, rectangles, max_generations=100, population_size=50, mutation_rate=0.1):
    def create_individual():
        """随机生成个体，同时保证数量限制"""
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
        #第一次版本以矩形数量为目标函数
        #第二次版本目标以矩形面积利用率为目标
        #后续或者是  加入面积利用率的权重或者优先考虑某些矩形类型
        placed = []
        type_count = {rect: 0 for rect in rectangles}  # 记录每种矩形已放置的数量
        total_area = 0
        for rect in individual:
            if rect[2:4] in rectangles:  # 确保类型合法
                if type_count[rect[2:4]] < rectangles[rect[2:4]]:  # 检查数量限制
                    if not is_overlapping(rect, placed) and is_within_bounds(rect):
                        placed.append(rect)
                        type_count[rect[2:4]] += 1
                        total_area += rect[2] * rect[3]  # 累加面积
        utilization_rate = total_area / (W * H)  # 面积利用率
        return utilization_rate, placed

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
        """变异操作，同时确保数量限制"""
        type_count = {rect: 0 for rect in rectangles}  # 记录每种矩形已放置的数量
        for i in range(len(individual)):
            if individual[i][2:4] in rectangles:
                type_count[individual[i][2:4]] += 1

        for i in range(len(individual)):
            if random.random() < mutation_rate:
                original = individual[i]
                rect_type = original[2:4]
                if type_count[rect_type] > rectangles[rect_type]:  # 数量超出，移除
                    individual[i] = None
                    type_count[rect_type] -= 1
                else:  # 随机生成新位置
                    x = random.randint(0, W - rect_type[0])
                    y = random.randint(0, H - rect_type[1])
                    individual[i] = (x, y, rect_type[0], rect_type[1])
        individual = [rect for rect in individual if rect is not None]  # 移除无效元素
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