import pandas as pd

def read_yard_names(file_path, sheet_name, column_name):
    """
    从 Excel 文件中读取堆场名称。

    参数:
        file_path (str): Excel 文件路径。
        sheet_name (str): 工作表名称。
        column_name (str): 包含堆场名称的列名。

    返回:
        list: 堆场名称列表。
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        if column_name not in df.columns:
            raise ValueError(f"列名 '{column_name}' 在工作表 '{sheet_name}' 中不存在。")
        return df[column_name].dropna().astype(str).str.strip().tolist()
    except Exception as e:
        print(f"读取堆场名称时出错: {e}")
        return []

def read_yard_data(file_path, sheet_name):
    """
    从 Excel 文件中读取堆场数据（堆场名称、车型等）。

    参数:
        file_path (str): Excel 文件路径。
        sheet_name (str): 工作表名称。

    返回:
        dict: 以堆场名称为键，车型列表为值的字典。
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        yard_data = {}
        for _, row in df.iterrows():
            yard_name = str(row['堆场名称']).strip()
            car_model = str(row['车型']).strip()
            if yard_name not in yard_data:
                yard_data[yard_name] = []
            if car_model not in yard_data[yard_name]:  # 避免重复添加
                yard_data[yard_name].append(car_model)
        return yard_data
    except Exception as e:
        print(f"读取堆场数据时出错: {e}")
        return {}

def generate_bin_priority_brands(yard_names, yard_data):
    """
    根据堆场名称和堆场数据生成 bin_priority_brands 列表。

    参数:
        yard_names (list): 堆场名称列表。
        yard_data (dict): 堆场数据字典。

    返回:
        list: 每个堆场的车型列表。
    """
    bin_priority_brands = []
    for yard_name in yard_names:
        if yard_name in yard_data:
            bin_priority_brands.append(yard_data[yard_name])
        else:
            bin_priority_brands.append([])  # 如果堆场没有车型，添加空列表
    return bin_priority_brands
#
# # 示例文件路径
# initial_file_path = r"C:\Users\zhuqiu\Desktop\第二次模型的输入数据.xlsx"  # 初始 Excel 文件，包含堆场名称
# output_file_path = r"C:\Users\zhuqiu\Desktop\result1.xlsx"   # 输出的 Excel 文件，包含堆场数据
#
# # 读取堆场名称
# yard_names = read_yard_names(initial_file_path, sheet_name='Yard_Areas', column_name='yard_names')
#
# # 读取堆场数据
# yard_data = read_yard_data(output_file_path, sheet_name='车型分布详情')
#
# # 生成 bin_priority_brands
# bin_priority_brands = generate_bin_priority_brands(yard_names, yard_data)
#
# # 打印结果
# print(bin_priority_brands)


# 定义 Rectangle 类
# class Rectangle:
#     def __init__(self, width, length, id, brand):
#         self.width = width
#         self.length = length
#         self.id = id
#         self.brand = brand
#
#     def __repr__(self):
#         return f"Rectangle(width={self.width}, length={self.length}, id={self.id}, brand={self.brand})"

