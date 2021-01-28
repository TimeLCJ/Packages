# coding:utf-8

import cv2
import time
import numpy as np
# 选取摄像头，0为笔记本内置的摄像头，1,2···为外接的摄像头
cap = cv2.VideoCapture(0)
# cap.set(3, 3840)
# cap.set(4, 1080)
# cap.set(3,2560)
# cap.set(4,720)
cap.set(3, 1280)
cap.set(4, 480)
# cap.set(3, 2560)
# cap.set(4, 960)
# cap.set(cv2.CAP_PROP_EXPOSURE, -6)
# cap.set(cv2.CAP_PROP_FPS, 50)
# cap.set(cv2.CAP_PROP_HUE, 20)
# cv2.namedWindow('frame')
# cv2.createTrackbar('expose time', 'frame', 6, 100, lambda x: None)
# cv2.createTrackbar('brightness', 'frame', 0, 100, lambda x: None)
# cv2.createTrackbar('contrast', 'frame', 0, 100, lambda x: None)
# # cv2.createTrackbar('hue', 'frame', 0, 100, lambda x: None) # 色调不能调
# # cv2.createTrackbar('saturation', 'frame', 64, 200, lambda x: None)
# cv2.createTrackbar('temperature', 'frame', 4600, 6000, lambda x: None)
# cv2.createTrackbar('sharpness', 'frame', 2, 100, lambda x: None)
# cv2.createTrackbar('1', 'frame', 1, 10, lambda x: None)
# cv2.createTrackbar('2', 'frame', 1, 10, lambda x: None)

# 读取视频流
while True:
    # expose_time = cv2.getTrackbarPos('expose time', 'frame')
    # brightness = cv2.getTrackbarPos('brightness', 'frame')
    # contrast = cv2.getTrackbarPos('contrast', 'frame')
    # # hue = cv2.getTrackbarPos('hue', 'frame')
    # # saturation = cv2.getTrackbarPos('saturation', 'frame')
    # temperature = cv2.getTrackbarPos('temperature', 'frame')
    # sharpness = cv2.getTrackbarPos('sharpness', 'frame')
    # a = cv2.getTrackbarPos('1', 'frame')
    # b = cv2.getTrackbarPos('2', 'frame')

    # cap.set(cv2.CAP_PROP_EXPOSURE, expose_time)
    # cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    # cap.set(cv2.CAP_PROP_CONTRAST, contrast)
    # # cap.set(cv2.CAP_PROP_HUE, -hue)
    # # cap.set(cv2.CAP_PROP_SATURATION, saturation)
    # cap.set(cv2.CAP_PROP_TEMPERATURE, temperature)
    # cap.set(cv2.CAP_PROP_SHARPNESS, sharpness)
    # cap.set(44, -a)
    # cap.set(45, -b)

    ret, frame = cap.read()  # 获取一帧图像
    if ret:
        # frame = cv2.flip(frame, 1)  # 调整方向，可不写
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        # 显示读取视频
        cv2.imshow('frame', frame)
        # q键关闭
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    else:
        break

# 关闭流
cap.release()
cv2.destroyAllWindows()