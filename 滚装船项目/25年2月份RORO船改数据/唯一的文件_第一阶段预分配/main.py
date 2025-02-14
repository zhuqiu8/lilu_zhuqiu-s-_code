from gurobipy import Model, GRB, quicksum
from data.Input_Data.data_input_lambda import *
from data.Input_Data.data_input_Models import *
from data.Input_Data.data_input_Brands import *
from data.Input_Data.data_input_CarDATA import *
from data.Input_Data.data_input_yard_areas import *

# 调用函数
excel_path = r"C:\Users\zhuqiu\Desktop\25年2月份RORO船改数据\25年2月roro船\2月输入数据2月13日晚更新.xlsx"  # 替换为实际的 Excel 文件路径

output_file_models_dict = r"Output_Data\models_dict"  # 替换为实际的输出文件路径
models_dict=generate_models_dict_from_excel(excel_path, "Models", output_file_models_dict)  #车型数据输入


lambda1, lambda2, lambda3 = read_parameters_from_excel(excel_path, 'Lambda')  # 读取 Lambda 参数

output_file_brands_dict = r"Output_Data\brands_dict"  # 替换为实际的输出文件路径
brands_dict = generate_brands_dict(excel_path, 'Brands', output_file_brands_dict)

output_file_car_data = r"Output_Data\car_data"  # 替换为实际的输出文件路径
car_data, brands, models = generate_car_data_dict(excel_path, "Car_Data", output_file_car_data)
# car_data, brands, models = generate_car_data_dict(excel_path, "Car_Data", "Models", output_file_car_data)

output_file_yard_areas = r"Output_Data\yard_areas"  # 替换为实际的输出文件路径
num_yards, yard_areas = generate_yard_areas(excel_path, "Yard_Areas", output_file_yard_areas, area_column="Yard_Area", utilization_rate_column="Utilization_Rate")

yard_names = read_yard_names_from_excel(excel_path, "Yard_Areas", column_name='yard_names') #堆场名字
print(yard_names)
# 创建模型
model = Model("Vehicle_Yard_Allocation")

# 决策变量
x = model.addVars(
    range(num_yards),  # i: 堆场编号
    brands,  # j: 品牌编号
    models,  # k: 车型编号
    vtype=GRB.INTEGER,
    name="x"
)  # 每辆车分配到堆场的数量
y = model.addVars(
    range(num_yards),
    brands,
    vtype=GRB.BINARY,
    name="y"
)  # 品牌是否分配到堆场

z = model.addVars(
    range(num_yards),
    models,
    vtype=GRB.BINARY,
    name="z"
)

u = model.addVars(range(num_yards), vtype=GRB.CONTINUOUS, name="u")  # 堆场利用率

# # 目标函数：最大化堆场利用率，最小化品牌分散度
# # lambda1 = 0  # 堆场利用率权重
# lambda2 = 1  # 品牌分散权重
# lambda3 = 0.5  # 控制车型集中权重
model.setObjective(
    lambda1 * quicksum(u[i] for i in range(num_yards))
    -lambda2 * quicksum(y[i, j] for i in range(num_yards) for j in brands) -
    lambda3 * quicksum(z[i, k] for i in range(num_yards) for k in models),
    GRB.MAXIMIZE
)

# 约束条件
# 1. 面积约束：每个堆场车辆面积不能超过堆场面积
for i in range(num_yards):
    model.addConstr(
        quicksum(car_data[(j, k)][0] * x[i, j, k] for j, k in car_data.keys()) <= yard_areas[i],  #此处通过修改初始的面积输入值，来控制占用率
        name=f"yard_area_{i}"
    )

# 2. 每辆车必须被分配到一个堆场
for (j, k) in car_data.keys():
    model.addConstr(
        quicksum(x[i, j, k] for i in range(num_yards)) == car_data[(j, k)][1],
        name=f"car_allocation_{j}_{k}"
    )

# 对于y的约束   确保 0-0；1-1
for i in range(num_yards):
    for j in brands:
        model.addConstr(
            quicksum(x[i, j, k] for k in models if (j, k) in car_data) <=
            y[i, j] * sum(car_data[(j, k)][1] for k in models if (j, k) in car_data),
            name=f"brand_in_yard_{i}_{j}"
        )
# 确保解决1-0的可能
for i in range(num_yards):  # 遍历所有堆场
    for j in brands:  # 遍历所有品牌
        model.addConstr(
            y[i, j] <= quicksum(x[i, j, k] for k in models if (j, k) in car_data),  # 删除 q 的维度
            name=f"brand_existence_{i}_{j}"
        )
# 约束：如果车型 k 被分配到堆场 i，则 z[i, k] 为 1
for i in range(num_yards):
    for k in models:
        model.addConstr(
            quicksum(x[i, j, k] for j in brands if (j, k) in car_data) <=
            z[i, k] * sum(car_data[(j, k)][1] for j in brands if (j, k) in car_data),
            name=f"model_presence_{i}_{k}"
        )


# 堆场利用率定义
for i in range(num_yards):
    model.addConstr(
        u[i] == quicksum(car_data[(j, k)][0] * x[i, j, k] for j, k in car_data.keys()) / yard_areas[i],
        name=f"utilization_{i}"
    )

# 求解模型
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    print("\nOptimal Solution Found!")
    for i in range(num_yards):
        print(f"\nYard {i + 1}:")
        for j in brands:
            total_area = sum(car_data[(j, k)][0] * x[i, j, k].x for k in models if (j, k) in car_data)
            total_cars = sum(x[i, j, k].x for k in models if (j, k) in car_data)
            if total_cars > 0:
                print(f"  Brand {j}: Area = {total_area}, Cars = {total_cars}")
        print(f"  Utilization: {u[i].x * 100:.2f}%")
else:
    print("No Optimal Solution Found.")

import pandas as pd

results = []

# 1. 输出堆场分配的车辆情况，并保存到 Excel
# 总分配情况
if model.status == GRB.OPTIMAL:
    print("\nOptimal Solution Found!")
    results = []  # 用于保存总分配结果
    model_results = []  # 用于记录车型分布的详细信息

    for i in range(num_yards):  # 遍历堆场
        # 堆场总体利用率
        print(f"\nYard {yard_names[i]} (Yard {i + 1}):")
        yard_utilization = u[i].x * 100
        print(f"  Utilization: {yard_utilization:.2f}%")

        # 品牌分配信息
        for j in brands:
            total_area = sum(car_data[(j, k)][0] * x[i, j, k].x for k in models if (j, k) in car_data)
            total_cars = sum(x[i, j, k].x for k in models if (j, k) in car_data)

            # 确保品牌信息完整记录，即使 total_cars 为 0
            results.append({
                '堆场名称': yard_names[i],
                '堆场编号': i + 1,
                '品牌': brands_dict[j],
                '总放置车数': total_cars,
                '总占地面积 (sqm)': total_area,
                '利用率 (%)': yard_utilization
            })

            if total_cars > 0:
                print(f"  Brand {brands_dict[j]}: Area = {total_area:.2f}, Cars = {total_cars}")

        # 车型分布情况
        for k in models:
            total_cars = sum(x[i, j, k].x for j in brands if (j, k) in car_data)
            if total_cars > 0:
                model_area = sum(car_data[(j, k)][0] * x[i, j, k].x for j in brands if (j, k) in car_data)
                print(f"    Model {models_dict[k]}: Cars = {total_cars}, Area = {model_area:.2f}")
                model_results.append({
                    '堆场名称': yard_names[i],
                    '堆场编号': i + 1,
                    '车型': models_dict[k],
                    '放置的数量': total_cars,
                    '车总占地面积 (sqm)': model_area
                })

    # 保存结果到 Excel
    grouped_results = pd.DataFrame(results)
    detailed_model_results = pd.DataFrame(model_results)

    # 检查并创建目标目录
    output_dir = '第一阶段预分配/Result'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, '结果0.7场地利用率.xlsx')  # 可以更改
    with pd.ExcelWriter(file_path) as writer:
        grouped_results.to_excel(writer, sheet_name="总分配情况", index=False)
        detailed_model_results.to_excel(writer, sheet_name="车型分布详情", index=False)
    print(f"Results have been saved to '{file_path}'.")
else:
    print("No Optimal Solution Found.")
