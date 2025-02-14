import pandas as pd


def get_bin_sizes(path, sheet_name, length_column="length", width_column="width"):
    df = pd.read_excel(path, sheet_name=sheet_name)

    # 校验列是否存在
    if length_column not in df.columns or width_column not in df.columns:
        raise ValueError(f"Excel 文件中未找到指定的列：'{length_column}' 或 '{width_column}'")

    # 提取长和宽并生成 bin_sizes
    lengths = df[length_column].tolist()
    widths = df[width_column].tolist()
    return [(length, width) for length, width in zip(lengths, widths)]

#
# bin_sizes = get_bin_sizes(path=r"C:\Users\zhuqiu\Desktop\第二次模型的输入数据.xlsx", sheet_name="Yard_Areas",
#                               length_column="Length", width_column="Width")
# print(bin_sizes)
