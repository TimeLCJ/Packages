import cv2
import glob


def images_to_video(path):
    img_array = []

    for filename in glob.glob(path + '/*.jpg'):
        img = cv2.imread(filename)
        if img is None:
            print(filename + " is error!")
            continue
        img_array.append(img)

    # 图片的大小需要一致
    size = (640, 400)
    fps = 10
    out = cv2.VideoWriter('demo.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def main():
    path = "./E21103157_1_20201127T165813Z_20201127T170813Z_0002_img"
    images_to_video(path)


if __name__ == "__main__":
    main()