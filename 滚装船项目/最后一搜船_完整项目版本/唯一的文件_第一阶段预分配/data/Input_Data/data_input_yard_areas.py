# import pandas as pd
#
# # 读取 Excel 文件
# excel_path = r"第二次模型的输入数据.xlsx"  # 替换为您的文件路径
# sheet_name = "Yard_Areas"  # 替换为您的工作表名称
# df = pd.read_excel(excel_path, sheet_name=sheet_name)
#
# # 提取编号和面积
# yard_areas = df.iloc[:, 1].tolist()  # 获取第二列数据（面积）
# num_yards = len(yard_areas)  # 堆场数量
#
#
# # 输出结果
# with open("../Output_Data/yard_areas.py", "w") as f:
#     f.write(f"num_yards = {num_yards}  # 堆场数量\n")
#     f.write(f"yard_areas = {yard_areas}  # 每个堆场的面积\n")
#
# print("代码已成功保存为 yard_areas.py 文件")

import pandas as pd


def generate_yard_areas(path, sheet_name, out_file, area_column="面积", utilization_rate_column="面积使用率"):
    """
    读取 Excel 文件中的堆场面积和使用率，计算调整后的面积并输出到文件。

    :param path: Excel 文件路径
    :param sheet_name: 工作表名称
    :param out_file: 输出文件路径
    :param area_column: 面积列名称
    :param utilization_rate_column: 面积使用率列名称
    :return: 堆场数量和调整后的面积列表
    """
    # 读取 Excel 文件
    df = pd.read_excel(path, sheet_name=sheet_name)

    # 校验列是否存在
    if area_column not in df.columns or utilization_rate_column not in df.columns:
        raise ValueError(f"Excel 文件中未找到指定的列：'{area_column}' 或 '{utilization_rate_column}'")

    # 提取面积和面积使用率
    yard_areas = df[area_column].tolist()
    utilization_rates = df[utilization_rate_column].tolist()

    # 计算调整后的面积
    adjusted_areas = [area * rate for area, rate in zip(yard_areas, utilization_rates)]
    num_yards = len(yard_areas)  # 堆场数量

    # 输出结果
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"num_yards = {num_yards}  # 堆场数量\n")
        f.write(f"original_areas = {yard_areas}  # 原始面积\n")
        f.write(f"utilization_rates = {utilization_rates}  # 面积使用率\n")
        f.write(f"yard_areas = {adjusted_areas}  # 调整后的面积\n")

    print(f"代码已成功保存为 {out_file} 文件")

    return num_yards, adjusted_areas

# 示例调用，返回 num_yards 和 yard_areas

# excel_path = r"C:\Users\zhuqiu\Desktop\第二次模型的输入数据.xlsx"  # 替换为实际的 Excel 文件路径
# output_file = r"唯一的文件_第一阶段预分配/data/Output_Data"  # 替换为实际的输出文件路径
# num_yards, yard_areas = generate_yard_areas(excel_path, "Yard_Areas", output_file)
# excel_path = r"C:\Users\zhuqiu\Desktop\第二次模型的输入数据.xlsx"  # 替换为实际的 Excel 文件路径
#
# output_file_yard_areas = r"Output_Data\yard_areas"  # 替换为实际的输出文件路径
# num_yards, yard_areas = generate_yard_areas(excel_path, "Yard_Areas", output_file_yard_areas, area_column="Yard_Area", utilization_rate_column="Utilization_Rate")


def read_yard_names_from_excel(file_path, sheet_name, column_name):
    """
    从 Excel 文件的指定工作表中读取 yard_names 数据。

    参数:
        file_path (str): Excel 文件的路径。
        sheet_name (str): 工作表的名称。
        column_name (str): 包含 yard_names 数据的列名。

    返回:
        list: 包含 yard_names 的列表。
    """
    try:
        # 读取 Excel 文件的指定工作表
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # 检查指定的列是否存在
        if column_name not in df.columns:
            raise ValueError(f"列名 '{column_name}' 在工作表 '{sheet_name}' 中不存在。")

        # 提取 yard_names 数据并清理（去除空格等）
        yard_names = df[column_name].dropna().astype(str).str.strip().tolist()

        return yard_names

    except Exception as e:
        print(f"读取 Excel 文件时出错: {e}")
        return []