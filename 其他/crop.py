import os
import cv2
import shutil

img_path = './6_forcalib'
result_path = img_path+'_crop'
if os.path.exists(result_path):
    shutil.rmtree(result_path)
if not os.path.exists(result_path):
    os.makedirs(result_path)
    os.makedirs(os.path.join(result_path, 'left'))
    os.makedirs(os.path.join(result_path, 'right'))
files = os.listdir(img_path)
pic_count = 0
for file in files:
    img = cv2.imread(os.path.join(img_path, file))
    w = img.shape[1]
    leftimg = img[:, :int(w/2)]
    rightimg = img[:, int(w/2):]
    cv2.imwrite(os.path.join(result_path, 'left', str(pic_count)+'.png'), leftimg)
    cv2.imwrite(os.path.join(result_path, 'right', str(pic_count)+'.png'), rightimg)
    pic_count += 1

