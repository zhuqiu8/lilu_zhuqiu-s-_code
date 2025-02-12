# import pandas as pd
#
# # 读取Excel文件
# file_path = r"第二次模型的输入数据.xlsx" # 替换为你的Excel文件路径
# sheet_name = 'Brands'  # 替换为你的Sheet名称
# df = pd.read_excel(file_path, sheet_name=sheet_name)
#
# # 确认两列数据
# # 假设第一列是编号，第二列是品牌名称
# column1 = df.iloc[:, 0]  # 第一列
# column2 = df.iloc[:, 1]  # 第二列
#
# # 生成字典
# brands_dict = {row[0]: f'"{row[1]}"' for row in zip(column1, column2)}
#
# # 格式化为字符串
# result = "brands_dict = {\n"
# for k, v in brands_dict.items():
#     comment = f"  # {v.split('_')[0]}" if "_" in v else ""
#     result += f"    {k}: {v},{comment}\n"
# result += "}"
#
# # 保存为文件或打印
# print(result)
# with open("../Output_Data/brands_dict.py", "w", encoding="utf-8") as f:
#     f.write(result)

import pandas as pd


def generate_brands_dict(file_path, sheet_name, output_file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 确认两列数据
    column1 = df.iloc[:, 0]  # 第一列
    column2 = df.iloc[:, 1]  # 第二列

    # 生成字典
    brands_dict = {row[0]: row[1] for row in zip(column1, column2)}

    # 格式化为字符串
    result = "brands_dict = {\n"
    for k, v in brands_dict.items():
        comment = f"  # {v.split('_')[0]}" if "_" in v else ""
        result += f"    {k}: '{v}',{comment}\n"  # 使用实际品牌名称作为值，且用单引号包裹
    result += "}"

    # 保存为文件
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"字典已保存到 {output_file_path}")

    # 返回字典
    return brands_dict  # 确保你返回字典

