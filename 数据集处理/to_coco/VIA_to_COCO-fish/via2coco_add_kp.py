import os
import cv2
import datetime
import json
import getArea
import os.path as osp
import shutil


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
    #in VIA annotations, keys are image name
    for img_id, key in enumerate(ann.keys()):
        ann_num = 0
        regions = ann[key]["regions"]
        shapes = [r['shape_attributes']['name'] for r in regions]
        if 'polygon' not in shapes:
            continue
        i1 = shapes.index('polygon')
        region_polygon = regions[i1]
        points_x = region_polygon['shape_attributes']['all_points_x']
        points_y = region_polygon['shape_attributes']['all_points_y']

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
        box = [min_x, min_y, max_x - min_x, max_y - min_y]
        # 仔细分析json分拣，VIA直接导出的COCO格式的json文件其实是不对的，使用mmdetection库进行训练时，根本不能识别出标注数据。
        # 其中非常明显的就是 segmentation不对。
        segmentation = get_segmenation(points_x, points_y)

        # keypoints
        kp_names = ['head', 'tail']
        keypoints = [0]*(len(kp_names)*3)
        ik = [i for i, r in enumerate(shapes) if r == 'point']
        num_keypoints = len(ik)
        if len(ik)>0:
            for i, kp_name in enumerate(kp_names):
                for ik_ in ik:
                    region_kp = regions[ik_]
                    if kp_name in region_kp["region_attributes"].values():
                        keypoints[i*3+0] = region_kp["shape_attributes"]["cx"]
                        keypoints[i*3+1] = region_kp["shape_attributes"]["cy"]
                        keypoints[i*3+2] = 2
                        break

        # make annotations info and storage it in coco_output['annotations']
        ann_info = create_annotation_info(ann_id, img_id, cat_id, iscrowd, area, box,
                                          segmentation, keypoints, num_keypoints)
        coco_output['annotations'].append(ann_info)
        ann_id = ann_id + 1
        ann_num += 1

        if ann_num > 0:
            filename = ann[key]['filename']
            print(filename)
            img = cv2.imread(osp.join(imgdir, filename))
            # make image info and storage it in coco_output['images']
            image_info = create_image_info(img_id, os.path.basename(filename), img.shape[:2])
            coco_output['images'].append(image_info)
            shutil.copy(osp.join(imgdir, filename), osp.join(result_dir, 'imgs', filename))
        else:
            num_invalid_images += 1
    print('total invalid image number is {}'.format(num_invalid_images))

    return coco_output


if __name__== '__main__':
    # img_path = '../fish_video/datasets_via_json/henze/train/' #改成自己的图片路径
    # anno_path = '../fish_video/datasets_via_json/henze/train_via_region_data.json' #自己的标注文件的路径。注意这里不是使用的VIA导出的coco格式文件，而是单纯的json格式文件。
    # result_path = '../henze_coco/annotations/instances_train.json' #输出，结果文件
    img_path = './data/hetun.5.11/imgs_selected4/' #改成自己的图片路径
    anno_path = './data/hetun.5.11/via_selected4.json' #自己的标注文件的路径。注意这里不是使用的VIA导出的coco格式文件，而是单纯的json格式文件。
    result_dir = './data1/hetun.5.11'
    result_img_dir = osp.join(result_dir, 'imgs')
    if not osp.exists(result_img_dir):
        os.makedirs(result_img_dir)
    result = convert(img_path, anno_path, result_dir)
    #把结果导出呈json文件。
    with open(osp.join(result_dir, 'coco_kp.json'), 'w') as file_obj:
        json.dump(result, file_obj)

