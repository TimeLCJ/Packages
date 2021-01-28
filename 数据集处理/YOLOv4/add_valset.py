import xml.etree.ElementTree as ET
import os

#classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
classes = ['oboat', 'sboat', 'dontcare']

def convert_annotation(image_id, list_file):
    in_file = open('./distribution_different_with_trianset/label/%s.xml'%(image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

image_set = 'val'
imgdir = './distribution_different_with_trianset/img'

list_file = open('%s.txt'%(image_set), 'a')
for image_name in os.listdir(imgdir):
    image_id = image_name[:-4]
    list_file.write('%s.jpg'%(image_id))
    convert_annotation(image_id, list_file)
    list_file.write('\n')
list_file.close()