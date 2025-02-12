#
import pandas as pd

def generate_car_data_dict(path, sheet_name, out_file):
    """
    从 Excel 文件中读取数据并生成 car_data 字典，同时生成品牌和车型的唯一索引。

    参数:
        path (str): Excel 文件路径。
        sheet_name (str): 数据工作表名称。
        out_file (str): 输出文件路径。

    返回:
        tuple: (car_data 字典, 品牌集合, 车型集合)
    """
    # 读取 Excel 文件
    df = pd.read_excel(path, sheet_name=sheet_name)

    # 确保列名正确
    df.columns = ["Brand", "Model", "length", "width", "Area_per_Car", "Quantity"]

    # 创建 car_data 字典
    car_data = {}

    # 为品牌生成唯一索引
    brand_indices = {brand: idx for idx, brand in enumerate(df["Brand"].unique())}

    # 为车型生成唯一索引
    model_indices = {model: idx for idx, model in enumerate(df["Model"].unique())}

    # 遍历每一行，构造键值对
    for _, row in df.iterrows():
        brand = row["Brand"]
        model = row["Model"]
        area = row["Area_per_Car"]
        quantity = row["Quantity"]

        # 获取品牌索引和车型索引
        brand_index = brand_indices[brand]
        model_index = model_indices[model]

        # 构造键和值
        key = (brand_index, model_index)
        value = [area, quantity]
        comment = f"  # {brand} {model}"

        # 插入到 car_data
        car_data[key] = value + [comment]

    # 获取所有品牌和车型的集合
    brands = set(brand_indices.values())  # 获取所有品牌索引
    models = set(model_indices.values())  # 获取所有车型索引

    # 格式化输出
    output = "car_data = {\n"
    for key, value in car_data.items():
        area_quantity = ", ".join(map(str, value[:2]))
        comment = value[2]
        output += f"    {key}: [{area_quantity}],{comment}\n"
    output += "}\n"

    # 保存到文件
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"转换完成！结果已保存到 {out_file}")

    # 返回 car_data 字典、品牌集合和车型集合
    return car_data, brands, models



# import pandas as pd
#
# def generate_car_data_dict(path, sheet_name, model_sheet_name, out_file):
#     """
#     从 Excel 文件中读取数据并生成 car_data 字典。
#
#     参数:
#         path (str): Excel 文件路径。
#         sheet_name (str): 数据工作表名称。
#         model_sheet_name (str): 车型索引工作表名称。
#         out_file (str): 输出文件路径。
#
#     返回:
#         tuple: (car_data 字典, 品牌集合, 车型集合)
#     """
#     # 读取 Excel 文件
#     df = pd.read_excel(path, sheet_name=sheet_name)
#     model_df = pd.read_excel(path, sheet_name=model_sheet_name)
#
#     # 确保列名正确
#     df.columns = ["Brand", "Model", "Area_per_Car", "Quantity"]
#     model_df.columns = ["Model_Index", "Model_Name"]
#
#     # 创建 car_data 字典
#     car_data = {}
#
#     # 获取所有品牌和车型的集合
#     brands = df["Brand"].unique()  # 所有品牌
#     models = df["Model"].unique()  # 所有车型
#
#     # 为品牌分配全局索引
#     brand_indices = {brand: idx for idx, brand in enumerate(brands)}
#
#     # 从 model sheet 中读取车型索引
#     model_indices = dict(zip(model_df["Model_Name"], model_df["Model_Index"]))
#
#     # 遍历每一行，构造键值对
#     for _, row in df.iterrows():
#         brand = row["Brand"]
#         model = row["Model"]
#         area = row["Area_per_Car"]
#         quantity = row["Quantity"]
#
#         # 获取品牌索引和车型索引
#         brand_index = brand_indices[brand]
#         model_index = model_indices.get(model, -1)  # 如果找不到车型索引，默认为 -1
#
#         # 构造键和值
#         key = (brand_index, model_index)
#         value = [area, quantity]
#         comment = f"  # {brand} {model}"
#
#         # 插入到 car_data
#         car_data[key] = value + [comment]
#
#     # 格式化输出
#     output = "car_data = {\n"
#     for key, value in car_data.items():
#         area_quantity = ", ".join(map(str, value[:2]))
#         comment = value[2]
#         output += f"    {key}: [{area_quantity}],{comment}\n"
#     output += "}\n"
#
#     # 保存到文件
#     with open(out_file, "w", encoding="utf-8") as f:
#         f.write(output)
#
#     print(f"转换完成！结果已保存到 {out_file}")
#
#     # 返回 car_data 字典、品牌集合和车型集合
#     return car_data, brands, models

#
#
#
#
#
# excel_path = r"C:\Users\zhuqiu\Desktop\第二次模型的输入数据.xlsx"  # 替换为实际的 Excel 文件路径
# output_file = r"D:\Github\RORO_Project\唯一的文件_第一阶段预分配\data\Output_Data"  # 替换为实际的输出文件路径
# car_data, brands, models = generate_car_data_dict(excel_path, "Car_Data", "Models", output_file)