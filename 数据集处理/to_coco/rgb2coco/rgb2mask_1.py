import cv2
import numpy as np
import os, glob

fish_color = [70, 130, 180]
fish_color = fish_color[::-1]

def rgb2masks(label_name):
    global fish_color
    lbl_id = os.path.split(label_name)[-1].split('.')[0]
    lbl = cv2.imread(label_name, 1)
    h, w = lbl.shape[:2]
    white_mask = np.ones((h, w, 3), dtype=np.uint8) * 255
    mask = (lbl == fish_color)
    mask = mask.all(-1)
    # leaf = lbl * mask[..., None]      # colorful leaf with black background
    # np.repeat(mask[...,None],3,axis=2)    # 3D mask
    leaf = np.where(mask[..., None], white_mask, 0)
    mask_name = './train/masks/' + lbl_id + '_fish_' + str(0) + '.png'
    cv2.imwrite(mask_name, leaf)


label_dir = './train/labels'
label_list = glob.glob(os.path.join(label_dir, '*.png'))
for label_name in label_list:
    rgb2masks(label_name)