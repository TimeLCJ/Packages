import os
import cv2
import datetime
import json
import getArea



def create_image_info(image_id, file_name, image_size,
                      date_captured=datetime.datetime.utcnow().isoformat(' '),
                      license_id=1, coco_url="", flickr_url=""):
    image_info = {
            "id": image_id,
            "file_name": file_name,
            "width": image_size[1], #原作者把这里写反了。造成了他原来的代码转化出来的标注文件生成的的mask维度不对。
            "height": image_size[0],#原作者把这里写反了。造成了他原来的代码转化出来的标注文件生成的的mask维度不对。
            "date_captured": date_captured,
            "license": license_id,
            "coco_url": coco_url,
            "flickr_url": flickr_url
    }
    return image_info

def create_annotation_info(annotation_id, image_id, category_id, is_crowd,
                           area, bounding_box, segmentation):
    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "iscrowd": is_crowd,
        "area": area,# float
        "bbox": bounding_box,# [x,y,width,height]
        "segmentation": segmentation# [polygon]
    }
    return annotation_info

def get_segmenation(coord_x, coord_y):
    seg = []
    for x, y in zip(coord_x, coord_y):
        seg.append(x)
        seg.append(y)
    return [seg]

def convert(imgdir, annpath):
    '''
    :param imgdir: directory for your images
    :param annpath: path for your annotations
    :return: coco_output is a dictionary of coco style which you could dump it into a json file
    as for keywords 'info','licenses','categories',you should modify them manually
    '''
    coco_output = {}
    coco_output['info'] = {
        "description": "Example Dataset",
        "url": "",
        "version": "1.0",
        "year": 2019,
        "contributor": "Black Jack",
        "date_created": datetime.datetime.utcnow().isoformat(' ')
    }
    coco_output['licenses'] = [
        {
            "id": 1,
            "name": "Attribution-NonCommercial-ShareAlike License",
            "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
        }
    ]
    coco_output['categories'] = [
        {
        'id': 1,
        'name': 'fish',
        'supercategory': 'allFish',
        },
    ]
    coco_output['images'] = []
    coco_output['annotations'] = []

    ann = json.load(open(annpath))
    # annotations id start from zero
    ann_id = 0
    num_invalid_images = 0

    cat_id = 1 # 我直接默认所有类别为"fish"，所以只有一个cat_id，其值为1
    iscrowd = 0
    #in VIA annotations, keys are image name
    for img_id, key in enumerate(ann.keys()):
        regions = ann[key]["regions"]

        # for one image ,there are many regions,they share the same img id
        for region in regions:
            if region['shape_attributes']['name'] == "point":
                x = region['shape_attributes']['x']
                y = region['shape_attributes']['y']
                width = region['shape_attributes']['width']
                height = region['shape_attributes']['height']
                box = [x, y, width, height]

                area = 0
                segmentation = [[]]
                ann_info = create_annotation_info(ann_id, img_id, cat_id, iscrowd, area, box, segmentation)
                coco_output['annotations'].append(ann_info)
                ann_id = ann_id + 1


            # # 这里也需要修改。原作者是region['region_attributes']['label'],
            # # #但是其实应该是region['region_attributes']['supercategory_name']
            # cat = region['region_attributes']['type'] #我的返回的子类的编号，所以其实不需要这一段，
            # print(cat)
            # assert cat in ['fish',]# 如果你的返回的是子类名字。那么这一段就需要。assert cat in ['name1', 'name2', 'name3',...]
            # if cat == 'fish': # if cat == 'name1':
            #     cat_id = 1
            elif region['shape_attributes']['name'] == "polygon":
                points_x = region['shape_attributes']['all_points_x']
                points_y = region['shape_attributes']['all_points_y']

                # if filename == 'data2_385.0.png':
                #     print(len(points_x), len(points_y), 'polygonlen')

                assert len(points_x) == len(points_y), \
                    "in via json file polygon, length of all_points_x must equal to length of all_points_y. "


                area = getArea.GetAreaOfPolyGon(points_x, points_y)

                if not area:
                    continue

                min_x = min(points_x)
                max_x = max(points_x)
                min_y = min(points_y)
                max_y = max(points_y)
                box = [min_x, min_y, max_x-min_x, max_y-min_y]
                # 仔细分析json分拣，VIA直接导出的COCO格式的json文件其实是不对的，使用mmdetection库进行训练时，根本不能识别出标注数据。
                #其中非常明显的就是 segmentation不对。
                segmentation = get_segmenation(points_x, points_y)
                # make annotations info and storage it in coco_output['annotations']
                ann_info = create_annotation_info(ann_id, img_id, cat_id, iscrowd, area, box, segmentation)
                coco_output['annotations'].append(ann_info)
                ann_id = ann_id + 1

        if ann_id > 0:
            filename = ann[key]['filename']
            print(filename)
            img = cv2.imread(imgdir + filename)
            # make image info and storage it in coco_output['images']
            image_info = create_image_info(img_id, os.path.basename(filename), img.shape[:2])
            coco_output['images'].append(image_info)
        else:
            num_invalid_images += 1
    print('total invalid image number is {}'.format(num_invalid_images))

    return coco_output


if __name__== '__main__':
    # img_path = '../fish_video/datasets_via_json/henze/train/' #改成自己的图片路径
    # anno_path = '../fish_video/datasets_via_json/henze/train_via_region_data.json' #自己的标注文件的路径。注意这里不是使用的VIA导出的coco格式文件，而是单纯的json格式文件。
    # result_path = '../henze_coco/annotations/instances_train.json' #输出，结果文件
    img_path = '../total/' #改成自己的图片路径
    anno_path = '../total/via_rectified.json' #自己的标注文件的路径。注意这里不是使用的VIA导出的coco格式文件，而是单纯的json格式文件。
    result_path = '../coco_box.json' #输出，结果文件
    result = convert(img_path, anno_path)
    #把结果导出呈json文件。
    with open(result_path, 'w') as file_obj:
        json.dump(result, file_obj)