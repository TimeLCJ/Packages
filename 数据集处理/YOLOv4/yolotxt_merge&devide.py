import os
import cv2
import shutil
import random

if __name__ == '__main__':
    trainval_percent = 0.9
    train_percent = 0.8
    rootdir_list = ['./hengze', './huizhou']
    result_dir = './merged'
    result_imgdir = os.path.join(result_dir, 'img')
    if not os.path.exists(result_imgdir):
        os.makedirs(result_imgdir)

    label_list = []
    for rootdir in rootdir_list:
        # label merge
        with open(os.path.join(rootdir, 'all.txt'), 'r') as f:
            label_list += f.readlines()

        # image copy
        imgdir = os.path.join(rootdir, 'img')
        for imgname in os.listdir(imgdir):
            shutil.copy(os.path.join(imgdir, imgname), os.path.join(result_imgdir, imgname))

    # label divide
    num = len(label_list)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    ftest = open(result_dir + '/test.txt', 'w')
    ftrain = open(result_dir + '/train.txt', 'w')
    fval = open(result_dir + '/val.txt', 'w')

    for i in list:
        label = label_list[i]
        if i in trainval:
            if i in train:
                ftrain.write(label)
            else:
                fval.write(label)
        else:
            ftest.write(label)

    ftrain.close()
    fval.close()
    ftest.close()


