# coding:utf-8

import cv2
import time
import numpy as np
# 选取摄像头，0为笔记本内置的摄像头，1,2···为外接的摄像头
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
# cap.set(3,2560)
# cap.set(4,720)
cap.set(3, 1280)
cap.set(4, 480)
# cap.set(3, 3840)
# cap.set(4, 1080)
# cap.set(3, 2560)
# cap.set(4, 960)
# cap.set(cv2.CAP_PROP_EXPOSURE, -7)
# cap.set(cv2.CAP_PROP_FPS, 50)
# cap.set(cv2.CAP_PROP_HUE, 20)

# 创建VideoWriter类对象
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# size = (1280, 480)
print(cap.get(cv2.CAP_PROP_EXPOSURE))
out = cv2.VideoWriter('outVideo-'+time.strftime('%m-%d-%H-%M', time.localtime(time.time()))+'.avi', fourcc, fps, size)
# 读取视频流
while cap.isOpened():
    ret, frame = cap.read()  # 获取一帧图像
    if ret:
        # frame = cv2.flip(frame, 1)  # 调整方向，可不写
        out.write(frame)  # 写入视频对象
        # 显示读取视频
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('frame', frame)
        # q键关闭
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 关闭流
cap.release()
out.release()
cv2.destroyAllWindows()