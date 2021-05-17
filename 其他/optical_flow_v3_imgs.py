import numpy as np
import cv2
import os

# def gen_seq():
#     """Generate motion sequence with an object"""
#
#     scene = cv2.GaussianBlur(np.uint8(255*np.random.rand(400, 500)), (21, 21), 3)
#
#     h, w = 400, 400
#     step = 4
#     obj_mask = np.zeros((h, w), np.bool)
#     obj_h, obj_w = 50, 50
#     obj_x, obj_y = 175, 175
#     obj_mask[obj_y:obj_y+obj_h, obj_x:obj_x+obj_w] = True
#     obj_data = np.uint8(255*np.random.rand(obj_h, obj_w)).ravel()
#     imgs = []
#     for i in range(0, 1+w//step, step):
#         img = scene[:, i:i+w].copy()
#         img[obj_mask] = obj_data
#         imgs.append(img)
#
#     return imgs
#
# # generate image sequence
# imgs = gen_seq()

img_path = './withboat_concate'
img_names = os.listdir(img_path)
img_names.sort(key=lambda x: int(x[-10:-4]))
imgs = []
imgs_grey = []
for i in img_names:
    img = cv2.imread(os.path.join(img_path, i))[:, :640]
    imgs.append(img)
    imgs_grey.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))


# # display images
# for img in imgs:
#     cv2.imshow('Image', img)
#     k = cv2.waitKey(100) & 0xFF
#     if k == ord('q'):
#         break
# cv2.destroyWindow('Image')


def find_flows(imgs):
    """Finds the dense optical flows"""

    optflow_params = [0.5, 3, 15, 3, 5, 1.2, 0]
    prev = imgs[0]
    flows = []
    for img in imgs[1:]:
        flow = cv2.calcOpticalFlowFarneback(prev, img, None, *optflow_params)
        flows.append(flow)
        prev = img

    return flows

# find optical flows between images
flows = find_flows(imgs_grey)

# display flows
h, w = imgs[0].shape[:2]
hsv = np.zeros((h, w, 3), dtype=np.uint8)
hsv[..., 1] = 255

for flow, img in zip(flows, imgs):
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang*180/np.pi/2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    bgr = np.concatenate((bgr, img), axis=1)
    cv2.imshow('Flow', bgr)
    k = cv2.waitKey(2000) & 0xFF
    if k == ord('q'):
        break
cv2.destroyWindow('Flow')

# def label_flows(flows):
#     """Binarizes the flows by direction and magnitude"""
#
#     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#     flags = cv2.KMEANS_RANDOM_CENTERS
#     h, w = flows[0].shape[:2]
#
#     labeled_flows = []
#     for flow in flows:
#         flow = flow.reshape(h*w, -1)
#         comp, labels, centers = cv2.kmeans(flow, 2, None, criteria, 10, flags)
#         n = np.sum(labels == 1)
#         camera_motion_label = np.argmax([labels.size-n, n])
#         labeled = np.uint8(255*(labels.reshape(h, w) == camera_motion_label))
#         labeled_flows.append(labeled)
#     return labeled_flows
#
# # binarize the flows
# labeled_flows = label_flows(flows)
#
# # # display binarized flows
# # for labeled_flow in labeled_flows:
# #     cv2.imshow('Labeled Flow', labeled_flow)
# #     k = cv2.waitKey(100) & 0xFF
# #     if k == ord('q'):
# #         break
# # cv2.destroyWindow('Labeled Flow')
#
# def find_target_in_labeled_flow(labeled_flow):
#
#     labeled_flow = cv2.bitwise_not(labeled_flow)
#     bw = 10
#     h, w = labeled_flow.shape[:2]
#     border_cut = labeled_flow[bw:h-bw, bw:w-bw]
#     conncomp, stats = cv2.connectedComponentsWithStats(border_cut, connectivity=8)[1:3]
#     target_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
#     img = np.zeros_like(labeled_flow)
#     img[bw:h-bw, bw:w-bw] = 255*(conncomp == target_label)
#     return img
#
# for labeled_flow, img in zip(labeled_flows, imgs[:-1]):
#     target_mask = find_target_in_labeled_flow(labeled_flow)
#     display_img = img
#     contours, hie = cv2.findContours(target_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#     count = []
#     for contour in contours:
#         count.append(contour.shape[0])
#     ind = np.array(count).argsort()
#     max_ind = ind[-1]
#     display_img = cv2.drawContours(display_img, contours, max_ind, (0, 255, 0), 2)
#
#     # cv2.imshow('Detected Target', display_img)
#     # k = cv2.waitKey(2000) & 0xFF
#     # if k == ord('q'):
#     #     break