import os
import cv2
import datetime
import json
import getArea
import shutil

def convert(imgdir, annpath, result_path):
    '''
    :param imgdir: directory for your images
    :param annpath: path for your annotations
    :return: coco_output is a dictionary of coco style which you could dump it into a json file
    as for keywords 'info','licenses','categories',you should modify them manually
    '''
    via_output = {}
    # size = 10000
    ann = json.load(open(annpath))
    # annotations id start from zero

    num_invalid_images = 0
    #in VIA annotations, keys are image name
    for img_id, key in enumerate(ann.keys()):
        imgs_valid_list = os.listdir(imgdir)
        regions = ann[key]["regions"]
        filename = ann[key]['filename']
        size = ann[key]["size"]
        if filename not in imgs_valid_list:
            continue
        # img = cv2.imread(os.path.join(imgdir, filename))
        num_keyppoint = 0
        regions_new = []
        # for one image ,there are many regions,they share the same img id
        for region in regions:
            # # 这里也需要修改。原作者是region['region_attributes']['label'],
            # # #但是其实应该是region['region_attributes']['supercategory_name']
            # cat = region['region_attributes']['type'] #我的返回的子类的编号，所以其实不需要这一段，
            # print(cat)
            # assert cat in ['fish',]# 如果你的返回的是子类名字。那么这一段就需要。assert cat in ['name1', 'name2', 'name3',...]
            # if cat == 'fish': # if cat == 'name1':
            #     cat_id = 1
            cat_id = 1 # 我直接默认所有类别为"fish"，所以只有一个cat_id，其值为1
            iscrowd = 0
            if 'cx' in region['shape_attributes']:
                regions_new.append(region)
                num_keyppoint += 1
                continue
        if num_keyppoint > 0:
            print(filename)
        else:
            num_invalid_images += 1

        via_output[filename + str(size)] = {'filename': filename,
                                              'size': size,
                                              'regions': regions_new,
                                              "file_attributes": {}}
    print('total invalid image number is {}'.format(num_invalid_images))

    return via_output


if __name__== '__main__':
    # img_path = '../fish_video/datasets_via_json/henze/train/' #改成自己的图片路径
    # anno_path = '../fish_video/datasets_via_json/henze/train_via_region_data.json' #自己的标注文件的路径。注意这里不是使用的VIA导出的coco格式文件，而是单纯的json格式文件。
    # result_path = '../henze_coco/annotations/instances_train.json' #输出，结果文件
    img_path = './imgs_selected3' #改成自己的图片路径
    anno_path = './imgs_selected3/via_selected3.json' #自己的标注文件的路径。注意这里不是使用的VIA导出的coco格式文件，而是单纯的json格式文件。
    result_path = './imgs_selected3' #输出，结果文件
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    result = convert(img_path, anno_path, result_path)
    #把结果导出呈json文件。
    with open(os.path.join(result_path, 'via_selected3_kp.json'), 'w') as file_obj:
        json.dump(result, file_obj)