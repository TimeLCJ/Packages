# coding:utf-8
import os
import cv2
import numpy as np

video_path = 'D:/yujing/videos/zhenzhu2_u.mp4'
# 选取摄像头，0为笔记本内置的摄像头，1,2···为外接的摄像头
cap = cv2.VideoCapture(video_path)
cap.set(3,1280)
cap.set(4,480)


# 创建VideoWriter类对象
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('crop_'+os.path.split(video_path)[1], fourcc, fps, size)

i = 0
# 读取视频流
while cap.isOpened():
    ret, frame = cap.read()  # 获取一帧图像
    if ret:
        if i > 120:
            # frame = cv2.flip(frame, 1)  # 调整方向，可不写
            out.write(frame)  # 写入视频对象
    else:
        break
    i += 1
print(i)
# 关闭流
cap.release()
out.release()