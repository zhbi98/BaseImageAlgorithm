
from PIL import Image
from PIL import ImageTk

import math
import numpy as np
import matplotlib.pyplot as plt


def loadImage(path):
    image = Image.open(path)
    # image.show()
    return image


def imageToMatrix(image):
    matrix = np.asarray(image)
    # print(matrix)
    return matrix


def matrixToImage(matrix):
    image = Image.fromarray(matrix)
    return image


# If there are 0 - 1 values in the image matrix, 
# or there are floating point numbers, then the 
# fromarray method of Image will not be able to
# convert the matrix into an image
def matrixToImages(matrix):
    # convert matrix values into 
    # data types supported by fromarray
    image = Image.fromarray((matrix * 255).astype(np.uint8))
    return image


def power(value, n):
    result = 1

    if n == 0:
        result = 1
    else:
        for i in range(n):
            result = result * value
    
    return result


def imageLight(image, light):
    if light <= 8:
        light = 8
    if light >= 10:
        light = 10

    imagematrix = imageToMatrix(image)
    dark = imagematrix / power(2, light)
    dark = matrixToImages(dark)
    return dark


image = loadImage('./Sierra16.jpg')

image = imageLight(image, 9)
image.show()

# plt.figure('Image Brightness')
# plt.imshow(image)
# plt.show()
# image.show()
