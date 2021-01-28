import cv2
import numpy as np
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

def label_flow(flow):
    """Binarizes the flows by direction and magnitude"""

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    h, w = flow.shape[:2]

    labeled_flow = []
    flow = flow.reshape(h*w, -1)
    comp, labels, centers = cv2.kmeans(flow, 2, None, criteria, 10, flags)
    n = np.sum(labels == 1)
    camera_motion_label = np.argmax([labels.size-n, n])
    labeled_flow = np.uint8(255*(labels.reshape(h, w) == camera_motion_label))
    return labeled_flow


def find_target_in_labeled_flow(labeled_flow):

    labeled_flow = cv2.bitwise_not(labeled_flow)
    bw = 10
    h, w = labeled_flow.shape[:2]
    border_cut = labeled_flow[bw:h-bw, bw:w-bw]
    conncomp, stats = cv2.connectedComponentsWithStats(border_cut, connectivity=8)[1:3]
    target_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
    img = np.zeros_like(labeled_flow)
    img[bw:h-bw, bw:w-bw] = 255*(conncomp == target_label)
    return img


cap = cv2.VideoCapture("outVideo-10-20-16-25.mp4")
# cap = cv2.VideoCapture("../data/slow.flv")
ret, frame1 = cap.read()

prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255

while True:
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    # binarize the flows
    labeled_flow = label_flow(flow)
    target_mask = find_target_in_labeled_flow(labeled_flow)
    contours = cv2.findContours(target_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    display_img = cv2.drawContours(frame2, contours, -1, (0, 255, 0), 2)

    cv2.imshow('frame2', display_img)
    k = cv2.waitKey(1) & 0xff
    if k == ord('q'):
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png', frame2)
        cv2.imwrite('opticalhsv.png', bgr)
    prvs = next

cap.release()
cv2.destroyAllWindows()


