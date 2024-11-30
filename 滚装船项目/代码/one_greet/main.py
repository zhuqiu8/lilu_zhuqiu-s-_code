from Yards_Cars import *
from Max_rectangles import *
from Yards_Cars import Calculate_all_emission_scenarios

import pandas as pd



#测试每个堆场的排放布局
results = Calculate_all_emission_scenarios(all_rectangles, yards)


df = pd.DataFrame(results)
df.to_excel("results.xlsx", index=False)

