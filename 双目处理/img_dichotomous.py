import cv2
import os
import os.path as osp

img_dir = "./image1"
dst_dir = img_dir+'_left'
if not osp.exists(dst_dir):
    os.makedirs(dst_dir)

img_names = os.listdir(img_dir)
for img_name in img_names:
    img_path = osp.join(img_dir, img_name)
    img = cv2.imread(img_path)
    w = img.shape[1]
    imgl = img[:, :int(w/2)]
    cv2.imwrite(osp.join(dst_dir, img_name), imgl)
    print(f'save {img_name}')
