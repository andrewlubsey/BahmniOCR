import deskew
import cv2
import numpy as np
from matplotlib import pyplot as plt

from corner_detector import CornerDetector


def preprocess_image(image):
    """
    Reduce noise

    :param image: image array in numpy
    :return: the processed image
    """
    image = cv2.medianBlur(image, 3)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Binarisation
    processedimage = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    processedimage = cv2.medianBlur(processedimage, 3)
    return processedimage


def deskew_image(im, pim):
    cornerdetector = CornerDetector(pim)
    corners = cornerdetector.detect_corners()
    for i in range(0, len(corners)):
        corner = corners[i]
        nextcorner = corners[(i + 1) % len(corners)]
        cv2.circle(im, (corner[0], corner[1]), 25, (210, 210, 210), -1)
        cv2.circle(im, (corner[0], corner[1]), 27, (130, 210, 210), 4)
        cv2.line(im, tuple(corner), tuple(nextcorner), (130, 210, 210), 5)
    plt.imshow(im, cmap='gray')
    plt.show()
    deskewer = deskew.Deskewer(im, corners, 1.414)
    transformedimage = deskewer.deskew()
    return transformedimage


def debugPlot(array):
    plt.plot(np.arange(0, len(array), 1), array)
    plt.show()


# Erode and Dilate image
def dilate_erode(img, num_iterations):
    num_iterations = num_iterations if num_iterations else 1
    kernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(src=img, kernel=kernel, iterations=num_iterations)
    dilated_eroded = cv2.dilate(src=eroded, kernel=kernel, iterations=num_iterations)
    return dilated_eroded
