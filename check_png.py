import os
import re

path = './results/vehicle_obstacle_v1.3.3_tda4_sgm_benz_v3_for_align_datav2_tda4sgm/'

contents_list = os.listdir(path)

for data in contents_list:
    data_path = os.path.join(path, data)
    img_path = sorted([name for name in os.listdir(data_path) if name.endswith('.png')])
    num_list = []
    for png_name in img_path:
        regex = re.compile('\d+')
        num = int(max(regex.findall(png_name)))
        num_list.append(num)
    if not num_list:
        continue
    test_list = (x for x in range(num_list[0], num_list[-1]+1))
    loss_data = ''
    for i in test_list:    
        if i not in num_list:  
            # print(i)      
            loss_data = data
    if loss_data:
        print(loss_data)