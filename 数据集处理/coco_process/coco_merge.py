# -*- coding: utf-8 -*-
import sys
import os
import datetime
import random
import sys
import operator
import math
import numpy as np
import skimage.io
import matplotlib
from matplotlib import pyplot as plt
from collections import defaultdict, OrderedDict
import json

# 待合并的路径
FILE_DIR = "./coco_annos/"


def load_json(filenamejson):
    with open(filenamejson, 'r') as f:
        raw_data = json.load(f)
    return raw_data


file_count = 0
files = os.listdir(FILE_DIR)

root_data = {}
annotations_num = 0
images_num = 0
annotations_id = []
images = []

for x in range(len(files)):
    # 解析文件名字和后缀
    # print(str(files[x]))
    file_suffix = str(files[x]).split(".")[1]
    file_name = str(files[x]).split(".")[0]
    # 过滤类型不对的文件
    if file_suffix not in "json":
        continue
    # json文件计数
    file_count = file_count + 1
    # 组合文件路径
    filenamejson = FILE_DIR + str(files[x])
    print(filenamejson)

    # 读取文件
    if x == 0:
        # 第一个文件作为root
        root_data = load_json(filenamejson)
        # 为了方便直接在第一个json的id最大值基础上进行累加新的json的id
        annotations_num = len(root_data['annotations'])
        images_num = len(root_data['images'])
        # 拿到root的id
        for key1 in range(annotations_num):
            annotations_id.append(int(root_data['annotations'][key1]['id']))
        for key2 in range(images_num):
            images.append(int(root_data['images'][key2]['id']))
        print("{0}生成的json有 {1} 个图片".format(x, len(root_data['images'])))
        print("{0}生成的json有 {1} 个annotation".format(x, len(root_data['annotations'])))
    else:
        # 载入新的json
        raw_data = load_json(filenamejson)
        next_annotations_num = len(raw_data['annotations'])
        next_images_num = len(raw_data['images'])
        categories_num = len(raw_data['categories'])

        print("{0}生成的json有 {1} 个图片".format(x, len(raw_data['images'])))
        print("{0}生成的json有 {1} 个annotation".format(x, len(raw_data['annotations'])))

        # 对于image-list进行查找新id且不存在id库，直到新的id出现并分配
        old_imageid = []
        new_imageid = []
        for i in range(next_images_num):
            # 追加images的数据
            while (images_num in images):
                images_num += 1
            # 将新的id加入匹配库，防止重复
            images.append(images_num)
            # 保存新旧id的一一对应关系，方便annotations替换image_id
            old_imageid.append(int(raw_data['images'][i]['id']))
            new_imageid.append(images_num)
            # 使用新id
            raw_data['images'][i]['id'] = images_num
            root_data['images'].append(raw_data['images'][i])

        # 对于annotations-list进行查找新id且不存在id库，直到新的id出现并分配
        for i in range(next_annotations_num):
            # 追加annotations的数据
            while (annotations_num in annotations_id):
                annotations_num += 1
            # 将新的annotations_id加入匹配库，防止重复
            annotations_id.append(annotations_num)
            # 使用新id
            raw_data['annotations'][i]['id'] = annotations_num
            # 查到该annotation对应的image_id，并将其替换为已经更新后的image_id
            ind = int(raw_data['annotations'][i]['image_id'])
            # 新旧image_id一一对应,通过index旧id取到新id
            try:
                index = old_imageid.index(ind)
            except ValueError as e:
                print("error")
                exit()
            imgid = new_imageid[index]
            raw_data['annotations'][i]['image_id'] = imgid
            root_data['annotations'].append(raw_data['annotations'][i])

        # 统计这个文件的类别数--可能会重复，要剔除
        # 这里我的，categories-id在多个json文件下是一样的，所以没做处理
        raw_categories_count = str(raw_data["categories"]).count('name', 0, len(str(raw_data["categories"])))
        for j in range(categories_num):
            root_data["categories"].append(raw_data['categories'][j])
# 统计根文件类别数
temp = []
for m in root_data["categories"]:
    if m not in temp:
        temp.append(m)
root_data["categories"] = temp

print("共处理 {0} 个json文件".format(file_count))
print("共找到 {0} 个类别".format(str(root_data["categories"]).count('name', 0, len(str(root_data["categories"])))))

print("最终生成的json有 {0} 个图片".format(len(root_data['images'])))
print("最终生成的json有 {0} 个annotation".format(len(root_data['annotations'])))

json_str = json.dumps(root_data, ensure_ascii=False, indent=1)
# json_str = json.dumps(root_data)
with open('./coco_all_10.26/annotations/instances_val2017.json', 'w') as json_file:
    json_file.write(json_str)
# 写出合并文件

print("Done!") 