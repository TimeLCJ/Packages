from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

if __name__ == '__main__':
    class_list = {0:'fish'}
    img_path = 'total/1596093408039.jpg'
    img = np.array(Image.open(img_path))
    H, W, C = img.shape
    label_path = 'labels/1596093408039.txt'
    boxes = np.loadtxt(label_path, dtype=np.float).reshape(-1, 5)
    # xywh to topx,topy,w,h
    boxes[:, 1] = (boxes[:, 1] - boxes[:, 3] / 2) * W
    boxes[:, 2] = (boxes[:, 2] - boxes[:, 4] / 2) * H
    boxes[:, 3] *= W
    boxes[:, 4] *= H
    fig = plt.figure()
    ax = fig.subplots(1)
    for box in boxes:
        bbox = patches.Rectangle((box[1], box[2]), box[3], box[4], linewidth=2,
                                 edgecolor='r', facecolor="none")
        label = class_list[int(box[0])]
        # Add the bbox to the plot
        ax.add_patch(bbox)
        # Add label
        plt.text(
            box[1],
            box[2],
            s=label,
            color="white",
            verticalalignment="top",
            bbox={"color": 'g', "pad": 0},
        )
        ax.imshow(img)
    plt.show()