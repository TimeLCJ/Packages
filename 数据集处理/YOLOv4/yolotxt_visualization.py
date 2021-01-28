import os
import cv2

if __name__ == '__main__':
    image_dir = 'img'
    txt_path = './all.txt'
    save_dir = 'viz_images'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    with open(txt_path, 'r') as f:
        for i in f.readlines():
            imgname = i.split(' ')[0]
            bboxes = i.split(' ')[1:]
            img = cv2.imread(os.path.join(image_dir, imgname))
            for bbox in bboxes:
                info = [int(_) for _ in bbox.split(',')]
                cv2.rectangle(img, (info[0], info[1]), (info[2], info[3]), (255, 0, 0), thickness=2)
                cv2.putText(img, str(info[4]), (info[0], info[1]), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv2.imwrite(os.path.join(save_dir, imgname), img)
