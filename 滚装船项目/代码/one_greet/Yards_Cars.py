import numpy as np
from collections import defaultdict
from Max_rectangles  import *


'''
yards ：堆场面积集合
cars ：带排放的车辆集合
'''
yards = {'C1_1': np.array([9.2, 200]),      # 1区
         'C1_2': np.array([34, 150]),       # 1区
         'C1_3': np.array([52, 135]),       # 1区
         'C1_4': np.array([9.6, 150]),      # 1区
         'C1_5': np.array([18, 100]),       # 1区
         'R2': np.array([14.5, 250]),       # 5区
         'B8': np.array([34, 35]),          # 6区
         'R1': np.array([14.5, 270]),       # 2区
         'A7': np.array([34, 270]),         # 3区
         'A8': np.array([34, 100]),         # 4区
         'B3': np.array([34, 225]),         # 12区
         'R3': np.array([32, 450]),         # 9区
        #'F1': np.array([]),                # 7区
        #'G1':np.array([]),                 # 10区
         'Q1': np.array([14, 200])   # 11区
         }

#car = [宽， 长， 数量]
cars  = {
        'HMC_VENUE': np.array([2.2, 4.4, 241]),
        'HMC_ELANTRA_HEV': np.array([2.2, 5, 415]),
        'HMC_KONA_HEV':  np.array([2.2, 4.5, 458]),
        'HMC_KONE':  np.array([2.2, 4.5, 67]),
        'HMC_GV60': np.array([2.4, 5, 4]),
        'HMC_GV70': np.array([2.4, 5, 3]),
        'HMC_GV80': np.array([2.4, 5.4, 6]),
        'HMC_G80':  np.array([2.4, 5.5, 5]),

        # 'HIGER_KLQ6685GAEV':  np.array([]),
        # 'HIGER_KLQ6129GQ2':  np.array([]),
        # 'HIGER_KLQ6125GEV3':  np.array([]),
        # 'HIGER_KLQ6121YA':  np.array([]),

        # 'GOLDEN_DRAGON_XML6125CLE':  np.array([]),

        'CHERY_T19C':  np.array([1.825, 4.68, 100]),

        'DONGFENG_DONGFENG_BOX':  np.array([1.8, 4.2, 40]),

        'XIAOPENG_P71': np.array([2.5, 5.4, 55]),

        'KIA_STONIC': np.array([2.2, 4.5, 211]),
        'KIA_NIRO_HEV': np.array([2.2, 4.7, 358]),
        'KIA_SELTOS': np.array([2.2, 4.7, 199]),
        'KIA_PICANTO': np.array([2, 4, 438]),
        'KIA_EV9': np.array([2.4, 5.5, 14])

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
    for key, value in yards.items():  # 遍历堆场
        W, H = value
        print(f"堆场: {key}, 宽度 W={W}, 高度 H={H}")
        results[key] = {}

        for brand, cars_data in all_rectangles.items():  # 遍历品牌
            print(f"  品牌: {brand}")

            for car, data in cars_data.items():  # 遍历每个品牌下的车型
                width, length, count = data  # 获取宽度、长度和数量
                rectangles = {(width, length): count}  # 转换为字典格式
                max_count, placement_plan = max_rectangles(W, H, rectangles)

                print("    最大可放置数量：", max_count)
                print("    放置方案：")
                for x, y, rw, rh in placement_plan:
                    print(f"      小矩形放置在位置 ({x}, {y})，尺寸为 {rw} x {rh}")

                if brand not in results[key]:
                    results[key][brand] = {}

                results[key][brand][car] = {
                    "max_count": max_count,
                    "placement_plan": placement_plan
                }

    return results

