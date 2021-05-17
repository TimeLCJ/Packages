import cv2
import numpy as np
from matplotlib import pyplot as plt


def main():
    Overexpose = cv2.imread("image/800_1.jpg")
    underexpose = cv2.imread("image/800_0.jpg")
    #cv2.imshow("Over", Overexpose)
    #cv2.imshow("under", underexpose)
    plt.figure(1)

    plt.subplot(4,2,1)
    plt.imshow(Overexpose)

    plt.subplot(4,2,2)
    plt.imshow(underexpose)

    Overexpose = cv2.cvtColor(Overexpose, cv2.COLOR_BGR2HSV)
    underexpose = cv2.cvtColor(underexpose, cv2.COLOR_BGR2HSV)

    plt.subplot(4, 2, 3)
    chans = cv2.split(Overexpose)
    colors = ("b", "g", "r")
    for (chan, color) in zip(chans, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])

    plt.subplot(4, 2, 4)
    chans = cv2.split(underexpose)
    colors = ("b", "g", "r")
    for (chan, color) in zip(chans, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])

    plt.subplot(4, 2, 5)
    Overexpose[:, :, 2] = cv2.equalizeHist(Overexpose[:, :, 2])
    equalizeOver = cv2.cvtColor(Overexpose, cv2.COLOR_HSV2BGR)
    plt.imshow(equalizeOver)
    cv2.imwrite('./outVideo-12-21-16-05_img/out/equlizeOver.jpg', equalizeOver)
#    cv2.imshow('equalizeOver', equalizeOver)

    plt.subplot(4, 2, 6)
    underexpose[:, :, 2] = cv2.equalizeHist(underexpose[:, :, 2])
    equalizeUnder = cv2.cvtColor(underexpose, cv2.COLOR_HSV2BGR)
    plt.imshow(equalizeUnder)
    cv2.imwrite('./outVideo-12-21-16-05_img/out/equalizeunder.jpg', equalizeUnder)

    plt.subplot(4, 2, 7)
    chans = cv2.split(equalizeOver)
    colors = ("b", "g", "r")
    for (chan, color) in zip(chans, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])

    plt.subplot(4, 2, 8)
    chans = cv2.split(equalizeUnder)
    colors = ("b", "g", "r")
    for (chan, color) in zip(chans, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])

    plt.show()
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
