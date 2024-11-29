import numpy as np

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


def Yard(yards,cars):
    n=len(yards)
    for i in yards:
        S(i) = 
        for j in  cars: