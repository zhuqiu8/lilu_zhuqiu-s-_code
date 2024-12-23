import numpy as np
from collections import defaultdict
from Max_rectangles  import *
from genetic_algorithm_max_area import *

'''
yards ：堆场面积集合
cars ：带排放的车辆集合
'''
yards = {
    'C1_1': np.array([9.2, 200]).astype(int),      # 1区
    'C1_2': np.array([34, 150]).astype(int),       # 1区
    'C1_3': np.array([52, 135]).astype(int),       # 1区
    'C1_4': np.array([9.6, 150]).astype(int),      # 1区
    'C1_5': np.array([18, 100]).astype(int),       # 1区
    # 'R2': np.array([14.5, 250]).astype(int),       # 5区
    # 'B8': np.array([34, 35]).astype(int),          # 6区
    # 'R1': np.array([14.5, 270]).astype(int),       # 2区
    # 'A7': np.array([34, 270]).astype(int),         # 3区
    # 'A8': np.array([34, 100]).astype(int),         # 4区
    # 'B3': np.array([34, 225]).astype(int),         # 12区
    # 'R3': np.array([32, 450]).astype(int),         # 9区
    # #'F1': np.array([]),                           # 7区
    # #'G1': np.array([]),                           # 10区
    # 'Q1': np.array([14, 200]).astype(int)          # 11区
}

#car = [宽， 长， 数量]
cars  = {
    'HMC_VENUE': np.array([2.2, 4.4, 241]).astype(int),
    'HMC_ELANTRA_HEV': np.array([2.2, 5, 415]).astype(int),
    'HMC_KONA_HEV':  np.array([2.2, 4.5, 458]).astype(int),
    # 'HMC_KONE':  np.array([2.2, 4.5, 67]).astype(int),
    # 'HMC_GV60': np.array([2.4, 5, 4]).astype(int),
    # 'HMC_GV70': np.array([2.4, 5, 3]).astype(int),
    # 'HMC_GV80': np.array([2.4, 5.4, 6]).astype(int),
    # 'HMC_G80':  np.array([2.4, 5.5, 5]).astype(int),

    # # 'HIGER_KLQ6685GAEV':  np.array([]),
    # # 'HIGER_KLQ6129GQ2':  np.array([]),
    # # 'HIGER_KLQ6125GEV3':  np.array([]),
    # # 'HIGER_KLQ6121YA':  np.array([]),

    # # 'GOLDEN_DRAGON_XML6125CLE':  np.array([]),

    # 'CHERY_T19C':  np.array([1.825, 4.68, 100]).astype(int),

    # 'DONGFENG_DONGFENG_BOX':  np.array([1.8, 4.2, 40]).astype(int),

    # 'XIAOPENG_P71': np.array([2.5, 5.4, 55]).astype(int),

    # 'KIA_STONIC': np.array([2.2, 4.5, 211]).astype(int),
    # 'KIA_NIRO_HEV': np.array([2.2, 4.7, 358]).astype(int),
    # 'KIA_SELTOS': np.array([2.2, 4.7, 199]).astype(int),
    # 'KIA_PICANTO': np.array([2, 4, 438]).astype(int),
    # 'KIA_EV9': np.array([2.4, 5.5, 14]).astype(int)
}

# 分组车辆数据（按品牌）
brand_groups = defaultdict(list)
for car, specs in cars.items():
    brand = car.split('_')[0]  # 提取品牌名，通过字符串_分割
    brand_groups[brand].append(specs)

# 将所有品牌数据转为矩形格式
def all_brands_to_rectangles(brand_groups):
    all_rectangles = {}
    for brand, vehicles in brand_groups.items():
        # 将每个车型转换成 (宽度, 长度, 数量) 格式
        all_rectangles[brand] = {car: (spec[0], spec[1], spec[2]) for car, spec in zip(brand, vehicles)}
    return all_rectangles
# 将所有品牌数据转为矩形格式
# def all_brands_to_rectangles(brand_groups):
#     all_rectangles = {}
#     for brand, vehicles in brand_groups.items():
#         # 将每个车型转换成 (宽度, 长度, 数量) 格式
#         all_rectangles[brand] = {f"{brand}_{i}": (spec[0], spec[1], spec[2]) for i, spec in enumerate(vehicles)}
#     return all_rectangles



# 转换所有品牌车辆信息
all_rectangles = all_brands_to_rectangles(brand_groups)

# 计算每个堆场排放车辆的数量及放置方案
def Calculate_all_emission_scenarios(all_rectangles, yards):
    results = {}
    for key, yard in yards.items():  # 遍历堆场
        W = int(yard[0])  # 获取宽度并转换为整数
        H = int(yard[1])  # 获取高度并转换为整数
        results[key] = {}
        # print(f'''堆场：{key}，面积：{W} x {H}''')
        for brand, cars_data in all_rectangles.items():  # 遍历品牌
            # print(f"  品牌: {brand}")

            for car, data in cars_data.items():  # 遍历每个品牌下的车型
                width, length, count = data  # 获取宽度、长度和数量
                rectangles = {(width, length): count}  # 转换为字典格式

                #调用装箱方法
                # max_count, placement_plan = max_rectangles(W, H, rectangles)

                max_count, placement_plan = genetic_algorithm_max_area(W, H, rectangles)

                # print(f"  车型: {car}")
                # print("    最大可放置数量：", max_count)
                # print("    放置方案：")
                # for x, y, rw, rh in placement_plan:
                    # print(f"      小矩形放置在位置 ({x}, {y})，尺寸为 {rw} x {rh}")

                if brand not in results[key]:
                    results[key][brand] = {}

                results[key][brand][car] = {
                    "max_count": max_count,
                    "placement_plan": placement_plan
                }

    return results

