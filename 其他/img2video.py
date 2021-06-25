import cv2
import glob
import os
import os.path as osp

def images_to_video(path):
    suffix = ['.jpg', '.png']
    img_array = []
    img_names = [i for i in os.listdir(path) if i[-4:] in suffix]
    img_names = sorted(img_names, key=lambda x:int(x[:-4]))
    for filename in img_names:
        img = cv2.imread(osp.join(path, filename))
        if img is None:
            print(filename + " is error!")
            continue
        img_array.append(img)

    # 图片的大小需要一致
    size = (1280, 480)
    fps = 10
    out = cv2.VideoWriter('demo.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def main():
    path = "./video_20210531101817"
    images_to_video(path)


if __name__ == "__main__":
    main()