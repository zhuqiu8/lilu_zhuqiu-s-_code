from gurobipy import Model, GRB

# 参数定义
P = 3   #堆场的数量
B = 4   #品牌的数量
I = 4   #品牌的数量集合

n_i =[20,30]   #品牌i的车辆总数
A_k =[200,400]   #第k个堆场的总面积
a_ij = [5,3]    #品牌i的第j辆车的占地面积

K = 3   #堆场的数量
L =  [10,20,30]   #堆场的长度集合
W =  [5,10,15]    #堆场的宽度集合

l_k =  []     #第k个堆场的长度（加上安全距离）
w_k =  []     #第k个堆场的宽度（加上安全距离）

l_kk = []     #第k个堆场的原始长度
w_kk = []     #第k个堆场的原始宽度

# 创建模型
model = Model("VehicleAllocation")

# 决策变量
x = model.addVars(I, max(J), K, vtype=GRB.BINARY, name="x")  # x_jk^i
y = model.addVars(I, K, vtype=GRB.BINARY, name="y")  # y_k^i

# 目标函数
model.setObjective(
    sum(f[i] * y[i] for i in range(n)) +
    sum(c[i][j] * x[i, j] for i in range(n) for j in range(m)),
    GRB.MINIMIZE
)

# 约束条件
# 客户需求约束
for j in range(m):
    model.addConstr(sum(x[i, j] for i in range(n)) >= d[j], name=f"Demand_{j}")

# 工厂产能约束
for i in range(n):
    model.addConstr(sum(x[i, j] for j in range(m)) <= y[i] * M[i], name=f"Capacity_{i}")

# 求解模型
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    print(f"Optimal objective value: {model.objVal}")
    for i in range(n):
        if y[i].x > 0.5:
            print(f"Build factory at location {i}")
        for j in range(m):
            if x[i, j].x > 0:
                print(f"  Transport {x[i, j].x} units from factory {i} to customer {j}")
else:
    print("No optimal solution found!")
