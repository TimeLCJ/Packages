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
_dir = "720"
camera_size = "2560"
video_filename = _dir+".mp4"
cap = cv2.VideoCapture("./video/"+video_filename)
if camera_size == "2560":
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
else:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pic_count = 0
path = "./calibrate_img/divided_" + _dir
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
    key = cv2.waitKey(50)
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


# calibrate
chess_size = 20
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((11*8, 3), np.float32)
objp[:, :2] = np.mgrid[0:11, 0:8].T.reshape(-1, 2)
objp = objp * chess_size

# Arrays to store object points and image points from all the images.
objpoints_L = []  # 3d point in real world space
imgpoints_L = []  # 2d points in image plane.
objpoints_R = []  # 3d point in real world space
imgpoints_R = []  # 2d points in image plane.

size = None
count = 0
valid_num = 0
while count < pic_count:
    count += 1
    fnameL = "./left/"+str(count)+".png"
    fnameR = "./right/"+str(count)+".png"
    imgL = cv2.imread(fnameL)
    imgR = cv2.imread(fnameR)
    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
    size = grayL.shape[::-1]
    retL, cornersL = cv2.findChessboardCorners(grayL, (11, 8), None)
    retR, cornersR = cv2.findChessboardCorners(grayR, (11, 8), None)
    if retL and retR:
        valid_num += 1
        objpoints_L.append(objp)
        sub_conersL = cv2.cornerSubPix(grayL,cornersL,(11,11),(-1,-1),criteria)
        imgpoints_L.append(sub_conersL)
        objpoints_R.append(objp)
        sub_conersR = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)
        imgpoints_R.append(sub_conersR)
        #########show conner#####################################

        imgL = cv2.drawChessboardCorners(imgL, (11, 8), sub_conersL, retL)
        cv2.imshow('img', imgL)
        cv2.waitKey(0)

print('Valid image num:', valid_num)
# valid_num = max(valid_num, max_image_for_calibrate)
# tmp = list(zip(objpoints_L, imgpoints_L, objpoints_R, imgpoints_R))
# random.shuffle(tmp)
# objpoints_L, imgpoints_L, objpoints_R, imgpoints_R = zip(*tmp)
# objpoints_L = objpoints_L[:valid_num]
# imgpoints_L = imgpoints_L[:valid_num]
# objpoints_R = objpoints_R[:valid_num]
# imgpoints_R = imgpoints_R[:valid_num]

ret, mtxL, distcoeffL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints_L, imgpoints_L, size, None, None)
ret, mtxR, distcoeffR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints_R, imgpoints_R, size, None, None)
print("Valid img count:"+str(count))

error_L = []
for i in range(len(objpoints_L)):
    imgpoints2, _ = cv2.projectPoints(objpoints_L[i], rvecsL[i], tvecsL[i], mtxL, distcoeffL)
    error = cv2.norm(imgpoints_L[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    error_L.append(error)
print(error_L)
error_R=[]
ret, mtxR, distcoeffR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints_R, imgpoints_R, size, None, None)
for i in range(len(objpoints_R)):
    imgpoints2, _ = cv2.projectPoints(objpoints_R[i], rvecsR[i], tvecsR[i], mtxR, distcoeffR)
    error = cv2.norm(imgpoints_R[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    error_R.append(error)
print(error_R)


# stereoCalibrate
retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints_L,
                                                                                                 imgpoints_L,
                                                                                                 imgpoints_R,
                                                                                                 mtxL, distcoeffL,
                                                                                                 mtxR, distcoeffR,
                                                                                                 size,
                                                                                                 criteria=criteria,
                                                                                                 # flag = cv2.CALIB_FIX_INTRINSIC
                                                                                                 )
cameraMatrix1, roiL = cv2.getOptimalNewCameraMatrix(mtxL, distcoeffL, size, 1, size)
cameraMatrix2, roiR = cv2.getOptimalNewCameraMatrix(mtxR, distcoeffR, size, 1, size)
left_camera_matrix = cameraMatrix1
left_distortion = distCoeffs1

right_camera_matrix = cameraMatrix2
right_distortion = distCoeffs2

R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                  right_camera_matrix, right_distortion, size, R,
                                                                  T)
left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)


dic = {}
dic["size"]=size
dic["left_camera_matrix"] = left_camera_matrix.tolist()
dic["left_distortion"] = left_distortion.tolist()
dic["right_camera_matrix"] = right_camera_matrix.tolist()
dic["right_distortion"] = right_distortion.tolist()
dic["R"] = R.tolist()
dic["T"] = T.tolist()
file = open("para_"+_dir+".json", "w")
json.dump(dic, file)
os.chdir(old_dir)
file = open("para/para_"+_dir+".json", "w")
json.dump(dic, file)
print("parameter saved in para_"+_dir+".json!")