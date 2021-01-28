# coding:utf-8
import cv2
import time
import numpy as np

exposures = [-6, -8, -10]
# exposures = [-8, -10, -6]
# 选取摄像头，0为笔记本内置的摄像头，1,2···为外接的摄像头
cap = cv2.VideoCapture(0)
# cap.set(3, 3840)
# cap.set(4, 1080)
cap.set(3,2560)
cap.set(4,720)
print(cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))
print(cap.get(cv2.CAP_PROP_EXPOSURE))
print(cap.get(cv2.CAP_PROP_XI_AUTO_WB))
# 设置曝光
# cap.set(cv2.CAP_PROP_EXPOSURE, -11)
# 设置自动曝光
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
# print('设置自动曝光后cv2.CAP_PROP_AUTO_EXPOSURE的值：', cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))
# 设置手动曝光
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
print('设置自动曝光后cv2.CAP_PROP_AUTO_EXPOSURE的值：', cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))
print('设置自动曝光后cv2.CAP_PROP_EXPOSURE的值：', cap.get(cv2.CAP_PROP_EXPOSURE))
print('设置自动曝光后cv2.CAP_PROP_XI_AUTO_WB的值：', cap.get(cv2.CAP_PROP_XI_AUTO_WB))
# cap.set(3, 1280)
# cap.set(4, 480)
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
i = 0
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
    frames = []
    brightnesses = []
    expo = []
    for exposure in exposures:
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        ret, frame = cap.read()  # 获取一帧图像
        if ret:
            # frame = cv2.flip(frame, 1)  # 调整方向，可不写
            frame = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
            brightness = np.average(frame)
            frames.append(frame)
            brightnesses.append(brightness)
            expo.append(cap.get(cv2.CAP_PROP_EXPOSURE))
        else:
            break
    # result = np.vstack(frames)
    # # 显示读取视频
    # cv2.imshow('frame', result)
    # cv2.imshow('-6', frames[0])
    # cv2.imshow('-8', frames[1])
    result = cv2.putText(frames[2], str(expo[1]), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    cv2.imshow('-11', result)
    # q键关闭
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
# 关闭流
cap.release()
cv2.destroyAllWindows()