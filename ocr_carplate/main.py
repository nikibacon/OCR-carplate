import sys
import cv2
import numpy as np


def preprocess(gray):
    # 高斯平滑
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    # blur
    median = cv2.medianBlur(gaussian, 5)
    # Sobel
    sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=3)
    # 二值化
    ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
    # dilation then erosion
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
    # dilation
    dilation = cv2.dilate(binary, element2, iterations=1)
    # erosion 去掉細節
    erosion = cv2.erode(dilation, element1, iterations=1)
    # dilation 框明顯
    dilation2 = cv2.dilate(erosion, element2, iterations=3)
    cv2.imshow('dilation2', dilation2)
    cv2.waitKey(0)
    return dilation2


# def findplatenumberregion(img):
#     region = []
#     # 畫框
#     contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#     # filter 面積小
#     for i in range(len(contours)):
#         cnt = contours[i]
#         # 計算面積
#         area = cv2.contourArea(cnt)
#
#         # 不要小的
#         if area < 2000:
#             continue
#             (x, y, w, h) = cv2.boundingRect(c)
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#     return region


def detect(img):
    # color to grey
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dilation = preprocess(gray)

    # 畫框
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print('work1')

    # filter 面積小
    for i in range(len(contours)):
        cnt = contours[i]
        # 計算面積
        area = cv2.contourArea(cnt)
        print('work2')

        # 不要小的
        if area < 2500:
            print('work3')
            continue

        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        crop_img = img[y:y + h, x:x + w]

        print('work4')

    cv2.imshow('number plate', crop_img)
    cv2.imwrite('number_plate.jpg', crop_img)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)

    # 框
    cv2.imwrite('contours.png', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# if __name__ == '__car.py__':
imagePath = 'car.jpg'
img = cv2.imread('car.jpg')
detect(img)
