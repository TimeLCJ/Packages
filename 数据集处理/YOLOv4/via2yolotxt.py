import json
import os
import shutil
from collections import defaultdict

img_path = './GX010037.MP4.frames'
result_img_path = './img'
if not os.path.exists(result_img_path):
    os.makedirs(result_img_path)

name_box_id = defaultdict(list)
with open("./GX010037.MP4.frames/via_export_json.json", encoding='utf-8') as f:
    data = json.load(f)
print(f'the number of images is {len(data)}')
for image_id, key in enumerate(data.keys()):
    name = data[key]['filename']
    cat = 0
    regions = data[key]['regions']
    for region in regions:
        tmp = region['shape_attributes']
        x_min = int(tmp['x'])
        y_min = int(tmp['y'])
        x_max = x_min + int(tmp['width'])
        y_max = y_min + int(tmp['height'])
        name_box_id[name].append([x_min, y_min, x_max, y_max, cat])
print(f'the number of labeled images is {len(name_box_id)}')

f = open('all.txt', 'w')
for key in name_box_id.keys():
    shutil.copy(os.path.join(img_path, key), os.path.join(result_img_path, key))
    f.write(key)
    box_infos = name_box_id[key]
    for info in box_infos:
        box_info = " %d,%d,%d,%d,%d" % (
            info[0],info[1],info[2],info[3],info[4])
        f.write(box_info)
    f.write('\n')
f.close()