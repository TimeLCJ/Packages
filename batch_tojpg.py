import os
import cv2

img_path = './fish'
result_path = img_path+'_jpg'
if not os.path.exists(result_path):
    os.makedirs(result_path)
files = os.listdir(img_path)
for file in files:
    img = cv2.imread(os.path.join(img_path, file))
    cv2.imwrite(os.path.join(result_path, file+'.jpg'), img)