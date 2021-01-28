import numpy as np
import cv2
import json
import matplotlib.pyplot as plt

balance=0
#
# frame = cv2.imread("./20200929-160944.jpg")
# w = frame.shape[1]
# frame1 = frame[:,:int(w/2)]
# frame2 = frame[:,int(w/2):]


frame1 = cv2.imread("./calibrate_img/divided_720/left/1.png")
frame2 = cv2.imread("./calibrate_img/divided_720/right/1.png")


f = open("./HBV-1780-90_1_720.json","r")
dic = json.load(f)

size = tuple(dic["size"])
left_camera_matrix= np.array(dic["left_camera_matrix"])
right_camera_matrix= np.array(dic["right_camera_matrix"])
left_distortion= np.array(dic["left_distortion"])
right_distortion= np.array(dic["right_distortion"])
R = np.array(dic["R"])
T = np.array(dic["T"])

# 进行立体更正
R1, R2, P1, P2, Q,validPixROI1, validPixROI2  = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                  right_camera_matrix, right_distortion, size, R,
                                                                  T,flags=cv2.CALIB_ZERO_DISPARITY,alpha=balance)  #flags=CALIB_ZERO_DISPARITY   0
# 计算更正map
left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)

cv2.namedWindow("left")
cv2.namedWindow("right")
cv2.namedWindow("depth")
cv2.moveWindow("left", 0, 0)
cv2.moveWindow("right", 600, 0)
cv2.createTrackbar("num", "depth", 0, 30, lambda x: None)
cv2.createTrackbar("blockSize", "depth", 5, 30, lambda x: None)
cv2.createTrackbar("windowSize", "depth", 1, 20, lambda x: None)



# 添加点击事件，打印当前点的距离
def callbackFunc(e, x, y, f, p):
    if e == cv2.EVENT_LBUTTONDOWN:
        print(threeD[y][x])

point_list = []
def cal_dist(e,x,y,f,p):
    global point_list
    if e == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        point_list.append([x,y])
        if(len(point_list)==4):
            d1 = point_list[0][0] - point_list[1][0]
            x1 = np.array([point_list[0][0],point_list[0][1],d1,1]).T
            d2 = point_list[2][0] - point_list[3][0]
            x2 = np.array([point_list[2][0],point_list[2][1],d2,1]).T
            p1 = np.dot(Q,x1)
            p2 = np.dot(Q,x2)
            p1 = p1/p1[-1]
            p2 = p2/p2[-1]
            print(p1,p2)
            dist = np.linalg.norm(p1-p2)
            print(dist)
            point_list = []



cv2.setMouseCallback("depth", callbackFunc, None)
cv2.setMouseCallback("left",cal_dist,None)
cv2.setMouseCallback("right",cal_dist,None)
# 根据更正map对图片进行重构
img1_rectified = cv2.remap(frame1, left_map1, left_map2, cv2.INTER_LINEAR)
img2_rectified = cv2.remap(frame2, right_map1, right_map2, cv2.INTER_LINEAR)
#r1,r2,r3,r4 = validPixROI1
#img1_rectified =cv2.rectangle(img1_rectified,(r1,r2),(r3,r4),(255,0,0),1)
#r1,r2,r3,r4 = validPixROI2
#img2_rectified =cv2.rectangle(img2_rectified,(r1,r2),(r3,r4),(255,0,0),1)

# 将图片置为灰度图，为StereoBM作准备
imgL = cv2.cvtColor(img1_rectified, cv2.COLOR_BGR2GRAY)
imgR = cv2.cvtColor(img2_rectified, cv2.COLOR_BGR2GRAY)

while True:
    # 两个trackbar用来调节不同的参数查看效果
    num = cv2.getTrackbarPos("num", "depth") + 1
    blockSize = cv2.getTrackbarPos("blockSize", "depth")
    window_size = cv2.getTrackbarPos("windowSize", "depth")
    if blockSize % 2 == 0:
        blockSize += 1
    if blockSize < 5:
        blockSize = 5


    min_disp = 0
    num_disp = 16 * num - min_disp
    stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
                                   numDisparities=num_disp,
                                   blockSize=blockSize,
                                   P1=8 * 3 * window_size ** 2,
                                   P2=32 * 3 * window_size ** 2,
                                   disp12MaxDiff=1,
                                   uniquenessRatio=10,
                                   speckleWindowSize=100,
                                   speckleRange=32
                                   )

    disparity = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    disp = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # 将图片扩展至3d空间中，其z方向的值则为当前的距离
    threeD = cv2.reprojectImageTo3D(disparity.astype(np.float32), Q)
    img_total = np.concatenate((img1_rectified, img2_rectified), axis=1)
    img_total = cv2.line(img_total, (0, 50), (12800, 50), (0, 255, 0), 1)
    img_total = cv2.line(img_total, (0, 150), (12800, 150), (0, 255, 0), 1)
    img_total = cv2.line(img_total, (0, 250), (12800, 250), (0, 255, 0), 1)
    img_total = cv2.line(img_total, (0, 350), (12800, 350), (0, 255, 0), 1)
    cv2.imshow("total", img_total)
    cv2.imshow("left", img1_rectified)
    cv2.imshow("right", img2_rectified)
    cv2.imshow("depth", disp)



    key = cv2.waitKey(10)

    if key == ord("q"):
        break

cv2.destroyAllWindows()

