from gurobipy import Model, GRB, quicksum

# 参数
B = 3  # 品牌数量
J = [5, 7, 6]  # 每个品牌的车辆数量
K = 4  # 堆场数量
l = [[4, 5, 3, 6, 4], [3, 4, 3, 5, 4, 6, 2], [2, 4, 6, 5, 3, 4]]  # 每辆车的长度（每个[]表示一个品牌，里面的数字表示这个品牌车的长度）
w = [[2, 3, 1, 4, 2], [2, 3, 2, 4, 3, 3, 1], [3, 4, 3, 4, 2, 1]]  # 每辆车的宽度
A = [100*34, 270*14.5, 270*34, 225*34]  # 堆场总面积
L = [100, 270, 270, 225]  # 堆场长度（对应五个堆场的长度）
W = [34, 14.5, 34, 34]  # 堆场宽度（对应五个堆场的宽度）
alpha, beta = 0.5, 0.5  # 权重参数 alpha表示车辆集中度，beta表示面积未使用最低
M_large = 1000  # 大常数

# 创建模型
model = Model("VehicleAllocation")

###################
#   12/11/2024 15.29

#####    需要改进的是
# 减少决策变量的数量：你的模型中使用了 max(J) 作为车辆的数量，这会生成大量的变量，尤其是在遍历品牌和车辆时。如果可能的话，可以减少 J（例如，每个品牌的车辆数量或品牌数量较少），使问题规模变小。
# 删除冗余变量：考虑是否所有变量都是必要的。比如你可能不需要所有的 x、y、sigma、tau 等辅助变量。你可以尝试合并约束，或减少问题的复杂度。


# 决策变量
x = model.addVars(B, max(J), K, vtype=GRB.BINARY, name="x")  # 品牌i的第j辆车分配到堆场K
y = model.addVars(B, K, vtype=GRB.BINARY, name="y")  # 辅助变量
sigma = model.addVars(B, max(J), K, vtype=GRB.CONTINUOUS, name="sigma")  # x 坐标
tau = model.addVars(B, max(J), K, vtype=GRB.CONTINUOUS, name="tau")  # y 坐标
r = model.addVars(B, max(J), vtype=GRB.BINARY, name="r")  # 旋转变量
# x方向逻辑变量
m = model.addVars(max(J), max(J), B, B, vtype=GRB.BINARY, name="m")  # 表示车辆在x方向上的位置关系
# y方向逻辑变量
n = model.addVars(max(J), max(J), B, B, vtype=GRB.BINARY, name="n")  # 表示车辆在y方向上的位置关系

# 目标函数
model.setObjective(
    alpha * quicksum(y[i, k] for i in range(B) for k in range(K)) +
    beta * quicksum((A[k] - quicksum(l[i][j] * w[i][j] * x[i, j, k] for i in range(B) for j in range(J[i])))**2 for k in range(K)),
    GRB.MINIMIZE
)



#########################################
#         最简单的约束 都错了，那你回家吧
# 添加约束
# 1. 每辆车必须分配到一个堆场
for i in range(B):
    for j in range(J[i]):
        model.addConstr(quicksum(x[i, j, k] for k in range(K)) == 1)



#################################################################
#                如果错了   掌嘴好吧
# 2. 堆场面积限制
for k in range(K):
    model.addConstr(
        quicksum(l[i][j] * w[i][j] * x[i, j, k] for i in range(B) for j in range(J[i])) <= A[k]
    )


#################################################################
#          天呐，应该是正确的
# 3. 辅助变量的约束

#辅助变量之++++++车放在堆场的x决策和辅助变量y决策的联系
for i in range(B):
    for j in range(J[i]):
        for k in range(K):
            model.addConstr(x[i, j, k] <= y[i, k], f"c_{i}_{j}_{k}")

# 辅助变量————————确保每个品牌至少分配到一个堆场
for i in range(B):
    model.addConstr(
        quicksum(y[i, k] for k in range(K)) >= 1,
        name=f"brand_at_least_one_yard_{i}"
    )


#################################################################
#        检查了   md这么多
# 4. 品牌堆场限制，假设任意两个堆场就可以放完一个品牌的所有车辆，应该可以。。。。。。。。。。。。
for i in range(B):
    model.addConstr(quicksum(y[i, k] for k in range(K)) <= 2)  # 示例限制为 2 个堆场




##############################################################
#     已经检查
# 5. 各个矩形在堆场范围内。。。。。。。。。。。
for i in range(B):
    for j in range(J[i]):
        for k in range(K):
            model.addConstr(sigma[i, j, k] + (1 - r[i, j]) * w[i][j] + r[i, j] * l[i][j] <= L[k])
            model.addConstr(tau[i, j, k] + (1 - r[i, j]) * l[i][j] + r[i, j] * w[i][j] <= W[k])




############################################################
#   已经改正 并检查错误
# 6. 不重叠的约束 修正========
for i in range(B):
    for i_hat in range(B):  # 可以是相同品牌
        for delta in range(J[i]):
            for gamma in range(J[i_hat]):
                if i != i_hat or delta != gamma:  # 确保不是同品牌的同一辆车
                    for k in range(K):
                        # x 方向非重叠
                        model.addConstr(
                            sigma[i, delta, k] + (1 - r[i, delta]) * w[i][delta] + r[i, delta] * l[i][delta]
                            <= sigma[i_hat, gamma, k] + (1 - m[delta, gamma, i, i_hat]) * M_large,
                            name=f"no_overlap_x_{i}_{i_hat}_{delta}_{gamma}_{k}"
                        )

                        # y 方向非重叠
                        model.addConstr(
                            tau[i, delta, k] + (1 - r[i, delta]) * l[i][delta] + r[i, delta] * w[i][delta]
                            <= tau[i_hat, gamma, k] + (1 - n[delta, gamma, i, i_hat]) * M_large,
                            name=f"no_overlap_y_{i}_{i_hat}_{delta}_{gamma}_{k}"
                        )

                        # 逻辑关系
                        model.addConstr(
                            m[delta, gamma, i, i_hat] + m[gamma, delta, i_hat, i]
                            + n[delta, gamma, i, i_hat] + n[gamma, delta, i_hat, i] >= 1,
                            name=f"logic_relation_{i}_{i_hat}_{delta}_{gamma}"
                        )



# 求解模型
model.optimize()


# 输出结果
if model.status == GRB.OPTIMAL:
    print("Optimal solution found:")
    for i in range(B):
        for j in range(J[i]):
            for k in range(K):
                if x[i, j, k].X > 0.5:  # 如果车辆被分配到该堆场
                    orientation = "rotated" if r[i, j].X > 0.5 else "not rotated"
                    position_x = sigma[i, j, k].X
                    position_y = tau[i, j, k].X
                    print(f"Car {j} of Brand {i} assigned to Yard {k} ({orientation}) at position ({position_x:.2f}, {position_y:.2f})")
else:
    print("No optimal solution found.")


