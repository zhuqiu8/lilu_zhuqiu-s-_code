from every_epochs import  layout_items
from item import container,container_xianzhi,item_sizes,item_num




# 循环 布局 直到 pruduct里面没有产品了
for key,value in container.items():
    container_width,max_height=container_xianzhi(key)
    container_height, utilization=layout_items(item_sizes, item_num, container_width, max_height)
    
    print('堆场{value}的利用率为:{utilization},最大排样高度为：{container_height}')