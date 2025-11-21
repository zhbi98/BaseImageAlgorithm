
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


# The pixel value of the 
# floating - point index
# number in the original
# image using the bilinear
# interpolation algorithm 
# area
def removeFishEye(image, c):
    imagematrix = imageToMatrix(image)

    height = imagematrix.shape[0]
    width = imagematrix.shape[1]
    channel = imagematrix.shape[2]

    new = np.zeros((height, width, channel))

    radius = max(width, height) / 2

    if c > 3.2:
        c = 3.2
    circ = c * radius / math.pi

    for i in range(height):
        for j in range(width):
            y = i - height / 2
            x = j - width / 2

            r = math.sqrt(x * x + y * y)
            theta = math.atan(r / radius)
            
            if theta < 0.00001:
                k = 1
            else:
                k = circ * theta / r

            srcy = y * k
            srcx = x * k

            srcy = srcy + height / 2
            srcx = srcx + width / 2

            inty = int(srcy)
            floaty = srcy - inty
            
            intx = int(srcx)
            floatx = srcx - intx

            if inty == imagematrix.shape[0] - 1:
                inty_p = imagematrix.shape[0] - 1
            else:
                inty_p = inty + 1

            if intx == imagematrix.shape[1] - 1:
                intx_p = imagematrix.shape[1] - 1
            else:
                intx_p = intx +  1
     
            # Bilinear interpolation
            # f(i+u ,j+v) = (1-u) * (1-v) * f(i, j) + u * (1-v) * f(i+1, j) + (1-u) * v * f(i, j+1) + u * v * f(i+1, j+1)
            new[i, j] = (1 - floatx) * (1 - floaty) * imagematrix[inty, intx] + (1 - floatx) * floaty * imagematrix[inty_p, intx] + floatx * (1 - floaty) * imagematrix[inty, intx_p] + floatx * floaty * imagematrix[inty_p, intx_p]

    new = new / 255
    return matrixToImages(new)


photos = loadImage('./22.jpg')

image = removeFishEye(photos, 2)
image.show()

# plt.figure('Remove Fish Eye')
# plt.imshow(image)
# plt.show()
