from __future__ import division
import os
import cv2
import json
import argparse
import scipy.misc
import numpy as np
from tqdm import tqdm
from path import Path

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_dir", metavar='DIR', default='./outVideo-10-26-15-57_img',
                    help='path to original dataset')
parser.add_argument("--para-path", type=str, default='para_stereo_xiaomi_02_left_2rd.json', help='the parameter of left camera')
parser.add_argument("--dump-root", type=str, default='./rectified_2rd', help="Where to dump the data")
parser.add_argument("--height", type=int, default=256, help="image height")
parser.add_argument("--width", type=int, default=832, help="image width")


args = parser.parse_args()


def main():
    args.dump_root = Path(args.dump_root)
    args.dump_root.mkdir_p()

    f = open(args.para_path, "r")

    dic = json.load(f)
    size = tuple(dic["size"])
    left_camera_matrix = np.array(dic["left_camera_matrix"])
    left_distortion = np.array(dic["left_distortion"])
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(left_camera_matrix, left_distortion, size, 0)

    for i in os.listdir(args.dataset_dir):
        if i[-4:] == '.jpg':
            img = cv2.imread(os.path.join(args.dataset_dir, i))
            dst = cv2.undistort(img, left_camera_matrix, left_distortion, None, new_camera_matrix)
            cv2.imwrite(args.dump_root/i, dst)
    intrinsics = new_camera_matrix
    fx = intrinsics[0, 0]
    fy = intrinsics[1, 1]
    cx = intrinsics[0, 2]
    cy = intrinsics[1, 2]

    dump_cam_file = args.dump_root / 'cam.txt'
    with open(dump_cam_file, 'w') as f:
        f.write('%f,0.,%f,0.,%f,%f,0.,0.,1.' % (fx, cx, fy, cy))




if __name__ == '__main__':
    main()
