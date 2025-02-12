import pandas as pd
import os
def read_parameters_from_excel(path,sheet_name):
    # 确保传递的是正确的路径
    df = pd.read_excel(path, sheet_name=sheet_name, index_col=0)

    # 打印读取的 DataFrame
    print("读取的参数表：")
    print(df)

    # 去除重复的行
    df = df[~df.index.duplicated(keep='first')]

    # 提取参数，并设置默认值
    lambda1 = df.loc['lambda1', '值'] if 'lambda1' in df.index else 0
    lambda2 = df.loc['lambda2', '值'] if 'lambda2' in df.index else 1  # 默认值 1  品牌集中度权重
    lambda3 = df.loc['lambda3', '值'] if 'lambda3' in df.index else 0.5  # 车型集中度权重

    return lambda1, lambda2, lambda3

    # 打印当前工作目录，检查路径是否正确


print("当前工作目录:", os.getcwd())

# # 使用绝对路径指定 Excel 文件
# excel_path = "D:/Github/RORO_Project/唯一的文件_第一阶段预分配/data/Input_Data/第二次模型的输入数据.xlsx"  # 替换为实际的 Excel 文件路径
#
# # 调用函数
# Lambda = read_parameters_from_excel(excel_path, 'Lambda')  # 读取 Lambda 参数
# print("读取的权重参数：", Lambda)