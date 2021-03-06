import os
import cv2
import time

video_path = 'zhoushang/大黄鱼06.mp4'
cap = cv2.VideoCapture(video_path)
result_path = os.path.join('picture', 'Larimichthys crocea6')
if not os.path.exists(result_path):
    os.makedirs(result_path)

fps = int(cap.get(cv2.CAP_PROP_FPS))
i = 0
while cap.isOpened():
    # Read next image
    success, image = cap.read()
    if success:
        if i % (fps*2) == 0:
            cv2.imwrite(os.path.join(result_path, str(i)+'.jpg'), image)
        i += 1
    else:
        break
# 关闭流
cap.release()