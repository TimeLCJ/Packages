import os
import cv2
import datetime
import json
import getArea
import os.path as osp
import shutil
import numpy as np

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
                           area, bounding_box, segmentation, keypoints,
                           num_keypoints):
    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "iscrowd": is_crowd,
        "area": area,# float
        "bbox": bounding_box,# [x,y,width,height]
        "segmentation": segmentation, # [polygon]
        "keypoints": keypoints,
        "num_keypoints": num_keypoints,
    }
    return annotation_info

def get_segmenation(coord_x, coord_y):
    seg = []
    for x, y in zip(coord_x, coord_y):
        seg.append(x)
        seg.append(y)
    return [seg]

def convert(imgdir, annpath, result_dir):
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
                "supercategory": "fish",
                "id": 1,
                "name": "fish",
                "keypoints":
                    [
                        "Head",
                        "Caudal",
                    ],
                "skeleton": [
                    [1, 2],
                ]
            }
        ]
    coco_output['images'] = []
    coco_output['annotations'] = []

    ann = json.load(open(annpath))
    # annotations id start from zero
    ann_id = 0
    num_invalid_images = 0

    cat_id = 1 # 我直接默认所有类别为"fish"，所以只有一个cat_id，其值为1
    iscrowd = 0
    kp_names = ['Head', 'Caudal']
    #in VIA annotations, keys are image name
    for img_id, key in enumerate(ann.keys()):
        ann_num = 0
        lab = ann[key]
        filename = lab["filename"]
        img_path = osp.join(imgdir, filename)
        scatter_kps = [
            (reg["region_attributes"]["keypoint"], reg["shape_attributes"]["cx"], reg["shape_attributes"]["cy"])
            # (kp_name, x, y)
            for reg in lab["regions"]
            if reg["shape_attributes"]["name"] == "point" and "keypoint" in reg["region_attributes"].keys()]

        mask_polygons = [list(zip(reg["shape_attributes"]["all_points_x"], reg["shape_attributes"]["all_points_y"]))
                         for reg in lab["regions"] if reg["shape_attributes"]["name"] == "polygon"]
        if len(mask_polygons) < 0 or not osp.exists(img_path):
            continue

        img = cv2.imread(img_path)
        for polygon in mask_polygons:
            points_x = []
            points_y = []
            for x,y in polygon:
                points_x.append(x)
                points_y.append(y)
            mask = np.zeros_like(img[:, :, 0])
            mask = cv2.fillPoly(img=mask, pts=[np.expand_dims(np.array(polygon), axis=1)], color=(1,))
            keypoints = []
            num_keypoints = 0
            for kp_name in kp_names:
                chosen = None
                candidates = [kp for kp in scatter_kps if kp[0] == kp_name]
                for kp in candidates:
                    if mask[kp[2], kp[1]] == 1:
                        chosen = [kp[1], kp[2], 2]  # (x, y, visibility)
                        num_keypoints += 1
                        break
                if chosen is None:
                    chosen = [0, 0, 0]
                keypoints.extend(chosen)

            assert len(points_x) == len(points_y), \
                "in via json file polygon, length of all_points_x must equal to length of all_points_y. "

            area = getArea.GetAreaOfPolyGon(points_x, points_y)

            if not area:
                continue

            min_x = min(points_x)
            max_x = max(points_x)
            min_y = min(points_y)
            max_y = max(points_y)
            box = [min_x, min_y, max_x - min_x, max_y - min_y]
            # 仔细分析json分拣，VIA直接导出的COCO格式的json文件其实是不对的，使用mmdetection库进行训练时，根本不能识别出标注数据。
            # 其中非常明显的就是 segmentation不对。
            segmentation = get_segmenation(points_x, points_y)


            # make annotations info and storage it in coco_output['annotations']
            ann_info = create_annotation_info(ann_id, img_id, cat_id, iscrowd, area, box,
                                              segmentation, keypoints, num_keypoints)
            coco_output['annotations'].append(ann_info)
            ann_id = ann_id + 1
            ann_num += 1

        if ann_num > 0:
            print(filename)
            # make image info and storage it in coco_output['images']
            image_info = create_image_info(img_id, os.path.basename(filename), img.shape[:2])
            coco_output['images'].append(image_info)
            shutil.copy(img_path, osp.join(result_dir, 'imgs', filename))
        else:
            num_invalid_images += 1
    print('total invalid image number is {}'.format(num_invalid_images))

    return coco_output


if __name__== '__main__':
    # img_path = '../fish_video/datasets_via_json/henze/train/' #改成自己的图片路径
    # anno_path = '../fish_video/datasets_via_json/henze/train_via_region_data.json' #自己的标注文件的路径。注意这里不是使用的VIA导出的coco格式文件，而是单纯的json格式文件。
    # result_path = '../henze_coco/annotations/instances_train.json' #输出，结果文件
    img_path = './data/fish/imgs' #改成自己的图片路径
    anno_path = './data/fish/fish.mask.keypoints.json' #自己的标注文件的路径。注意这里不是使用的VIA导出的coco格式文件，而是单纯的json格式文件。
    result_dir = './data1/fish'
    result_img_dir = osp.join(result_dir, 'imgs')
    if not osp.exists(result_img_dir):
        os.makedirs(result_img_dir)
    result = convert(img_path, anno_path, result_dir)
    #把结果导出呈json文件。
    with open(osp.join(result_dir, 'coco_kp.json'), 'w') as file_obj:
        json.dump(result, file_obj)

