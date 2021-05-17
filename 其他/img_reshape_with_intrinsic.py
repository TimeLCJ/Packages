from __future__ import division
import os
import argparse
import scipy.misc
import numpy as np
from tqdm import tqdm
from path import Path

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_dir", metavar='DIR', default='./rectified',
                    help='path to original dataset')
parser.add_argument("--dump-root", type=str, default='./reshaped', help="Where to dump the data")
parser.add_argument("--height", type=int, default=256, help="image height")
parser.add_argument("--width", type=int, default=832, help="image width")


args = parser.parse_args()


def get_intrinsic(base_dir, zoom_x, zoom_y):
    #print(zoom_x, zoom_y)
    calib_file = os.path.join(base_dir, 'cam.txt')
    with open(calib_file, 'r') as f:
        for line in f.readlines():
            filedata = np.array([float(x) for x in line.split(',')])

    intrinsic = np.reshape(filedata, (3, 3))
    intrinsic[0] *= zoom_x
    intrinsic[1] *= zoom_y
    return intrinsic

def load_image(img_file, args):
    img = scipy.misc.imread(img_file)
    zoom_y = args.height/img.shape[0]
    zoom_x = args.width/img.shape[1]
    img = scipy.misc.imresize(img, (args.height, args.width))
    return img, zoom_x, zoom_y

def main():
    args.dump_root = Path(args.dump_root)
    args.dump_root.mkdir_p()

    for i in os.listdir(args.dataset_dir):
        if i[-4:] == '.jpg':
            img, zoom_x, zoom_y = load_image(os.path.join(args.dataset_dir, i), args)
            scipy.misc.imsave(args.dump_root/i, img)
    intrinsics = get_intrinsic(args.dataset_dir, zoom_x, zoom_y)
    fx = intrinsics[0, 0]
    fy = intrinsics[1, 1]
    cx = intrinsics[0, 2]
    cy = intrinsics[1, 2]

    dump_cam_file = args.dump_root / 'cam.txt'
    with open(dump_cam_file, 'w') as f:
        f.write('%f,0.,%f,0.,%f,%f,0.,0.,1.' % (fx, cx, fy, cy))




if __name__ == '__main__':
    main()
