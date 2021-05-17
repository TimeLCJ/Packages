import cv2
import os
import numpy as np

image_path = './calibrate_img/divided_480'
result_path = image_path+'_concate'
if not os.path.exists(result_path):
    os.makedirs(result_path)
for i in range(1, 51):
    leftimg = cv2.imread(os.path.join(image_path, 'left', str(i)+'.png'))
    rightimg = cv2.imread(os.path.join(image_path, 'right', str(i) + '.png'))
    concateimg = np.concatenate((leftimg, rightimg), axis=1)
    cv2.imwrite(os.path.join(result_path, str(i)+'.png'), concateimg)

