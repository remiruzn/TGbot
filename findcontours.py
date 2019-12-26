import cv2
import numpy as np
from matplotlib import pyplot as plt
from findcar import segment
#

# Функция для нахождения контуров машины с использованием фильтра Собеля
def findContoursGradient(image, img_path):
    path = img_path
    img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)

    img = cv2.fastNlMeansDenoising(img)

    preparedSrc = img.astype(dtype=np.float32)/255


    def derivative(dx, dy, p_src):
        resolution = img.shape[0] * img.shape[1]

        if resolution < 1280 * 1280:
            kernelSize = 3
        elif resolution < 2000 * 20000:
            kernelSize = 5
        elif resolution < 3000 * 3000:
            kernelSize = 9
        else:
            kernelSize = 15

        if kernelSize == 3:
            kernelFactor = 1
        else:
            kernelFactor = 2

        kernelRows, kernelColumns = cv2.getDerivKernels(dx, dy, kernelSize, normalize=True)

        multipliedKernelRows = kernelRows * kernelFactor
        multipliedKernelColumns = kernelColumns * kernelFactor

        preparedSrc = cv2.sepFilter2D(p_src.copy(), cv2.CV_32FC1, multipliedKernelRows, multipliedKernelColumns)

        return preparedSrc


    gradX = derivative(1, 0, preparedSrc)
    gradY = derivative(0, 1, preparedSrc)


    result = cv2.magnitude(gradX, gradY)
    #result += 0.15


    mask = segment(path)
    result_masked = cv2.bitwise_and(result, result, mask=mask)

    result_masked = (result_masked*255).astype(np.uint8)


    return cv2.bitwise_not(result_masked)


# Функция записывает обрезаный контур авто в основную дирректорию
def carCnt(img_path):
    scr = cv2.imread(img_path)

    car_cnt = findContoursGradient(scr, img_path)

    cv2.imwrite("CNTS.jpg", car_cnt)

