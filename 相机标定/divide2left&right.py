import cv2
import numpy as np
import json
import os
import random
import time

max_image_for_calibrate = 50
get_image_interval = 87
#_dir = "1280"
#camera_size = "1280"
camera_size = "480"
video_filename = camera_size+".mp4"

cap = cv2.VideoCapture(video_filename)
if camera_size == "720":
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
else:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pic_count = 0
path = "./calibrate_img/divided_" + camera_size
if os.path.exists(path):
    def del_file(path_data):
        for i in os.listdir(path_data):
            file_data = path_data + "\\" + i
            if os.path.isfile(file_data):
                os.remove(file_data)
            else:
                del_file(file_data)
    del_file(path)
else:
    os.makedirs(path)
    os.makedirs(path+"/left")
    os.makedirs(path+"/right")
old_dir = os.getcwd()
os.chdir(path)
print(os.getcwd())
frame_count = 0
while cap.isOpened():
    flag, frame = cap.read()
    if not flag:
        break
    cv2.imshow("img", frame)
    key = cv2.waitKey(40)
    frame_count += 1
    if key == ord("g"):
    # if frame_count >= get_image_interval:
        frame_count = 0
        w = frame.shape[1]
        imgL = frame[:, :int(w/2)]
        imgR = frame[:, int(w/2):]
        pic_count += 1
        cv2.imwrite("left/" + str(pic_count) + ".png", imgL)
        cv2.imwrite("right/" + str(pic_count)+".png", imgR)
        print("Current image number:"+str(pic_count))
        if pic_count >= max_image_for_calibrate:
            break
    elif key == 27 or key == ord("q"):
        break
print("Number of total image:", pic_count)