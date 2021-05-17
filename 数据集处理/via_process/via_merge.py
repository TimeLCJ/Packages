import os
import cv2
import datetime
import json
import getArea
import shutil

def convert(imgdir, annpath, result_path, anno_kp_path):
    '''
    :param imgdir: directory for your images
    :param annpath: path for your annotations
    :return: coco_output is a dictionary of coco style which you could dump it into a json file
    as for keywords 'info','licenses','categories',you should modify them manually
    '''
    via_output = {}
    # size = 10000
    ann = json.load(open(annpath))
    ann_kp = json.load(open(anno_kp_path))
    # annotations id start from zero

    num_invalid_images = 0
    #in VIA annotations, keys are image name
    for img_id, key in enumerate(ann.keys()):
        imgs_valid_list = os.listdir(imgdir)
        regions = ann[key]["regions"]
        regions_kp = ann_kp[key]["regions"]
        filename = ann[key]['filename']
        size = ann[key]["size"]
        if filename not in imgs_valid_list:
            continue
        if key not in ann_kp:
            print(f'{key} not in kp anno')
            continue

        num_mask = 0
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
                continue
            points_x = region['shape_attributes']['all_points_x']
            points_y = region['shape_attributes']['all_points_y']

            # if filename == 'data2_385.0.png':
            #     print(len(points_x), len(points_y), 'polygonlen')

            assert len(points_x) == len(points_y), \
                "in via json file polygon, length of all_points_x must equal to length of all_points_y. "


            area = getArea.GetAreaOfPolyGon(points_x, points_y)

            if area <= 0:
                continue

            min_x = min(points_x)
            max_x = max(points_x)
            min_y = min(points_y)
            max_y = max(points_y)
            box = [min_x, min_y, max_x-min_x, max_y-min_y]
            # patch = img[min_y: max_y, min_x: max_x]
            # patch_name = filename[:-4]+'_'+str(num_mask)+'.jpg'
            # cv2.imwrite(os.path.join(result_path, patch_name), patch)
            points_x = [i - min_x for i in points_x]
            points_y = [i - min_y for i in points_y]
            region_new = {"shape_attributes": {"name": "polygon", "all_points_x": points_x, "all_points_y": points_y},
                        "region_attributes": {"type": "fish"}
                        }
            regions_new.append(region_new)
            num_mask += 1
        if num_mask > 0:
            shutil.copy(os.path.join(imgdir, filename), os.path.join(result_path, filename))
            print(filename)
        else:
            num_invalid_images += 1
        # add kp anno
        regions_new.extend(regions_kp)

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
    anno_path = './imgs_selected3/via_selected3_rectify.json' #自己的标注文件的路径。注意这里不是使用的VIA导出的coco格式文件，而是单纯的json格式文件。
    anno_kp_path = './via_kp_rectify.json'
    result_path = './imgs_selected4' #输出，结果文件
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    result = convert(img_path, anno_path, result_path, anno_kp_path)
    #把结果导出呈json文件。
    with open(os.path.join(result_path, 'via_selected4.json'), 'w') as file_obj:
        json.dump(result, file_obj)