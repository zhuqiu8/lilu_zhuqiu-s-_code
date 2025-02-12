import pandas as pd
import os

def generate_models_dict_from_excel(path, sheet_name, out_file):
    """
    根据 Excel 文件生成 models_dict 并保存为 Python 文件。

    :param path:
    :param sheet_name: str, Excel 的 Sheet 名称
    :param out_file: str, 输出 Python 文件路径
    """
    # 确保输出目录存在，如果不存在则创建
    output_dir = os.path.dirname(out_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建目录: {output_dir}")
    try:
        # 读取 Excel 文件
        df = pd.read_excel(path, sheet_name=sheet_name)

        # 确认两列数据
        # 假设第一列是编号，第二列是品牌名称
        column1 = df.iloc[:, 0]  # 第一列
        column2 = df.iloc[:, 1]  # 第二列

        # 生成字典
        models_dict = {row[0]: f'"{row[1]}"' for row in zip(column1, column2)}

        # 格式化为字符串
        result = "models_dict = {\n"
        for k, v in models_dict.items():
            comment = f"  # {v.split('_')[0]}" if "_" in v else ""
            result += f"    {k}: {v},{comment}\n"
        result += "}"

        # 保存为 Python 文件
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(result)

        print("models_dict 已生成并保存到文件:", out_file)

        return models_dict

    except Exception as e:
        print("生成 models_dict 失败，错误信息：", e)

# excel_path = r"C:\Users\zhuqiu\Desktop\第二次模型的输入数据.xlsx"  # 替换为实际的 Excel 文件路径
# output_file = "Input_Data"  # 替换为实际的输出文件路径
# models_dict=generate_models_dict_from_excel(excel_path, "Models", output_file)  #车型数据输入