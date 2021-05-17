import os
import cv2
import time

video_path = 'outVideo-12-21-16-05.mp4'
cap = cv2.VideoCapture(video_path)
result_path = video_path[:-4]+'_img'
if not os.path.exists(result_path):
    os.makedirs(result_path)

i = 0
while cap.isOpened():
    # Read next image
    success, image = cap.read()
    if success:
        if i % 100 == 0:
            cv2.imwrite(os.path.join(result_path, str(i)+'.jpg'), image)
        # cv2.imwrite(os.path.join(result_path, str(i) + '.jpg'), image)
        i += 1
    else:
        break
# 关闭流
cap.release()