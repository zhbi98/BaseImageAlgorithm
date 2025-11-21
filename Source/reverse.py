
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


def imageReverse(image):
    imagematrix = imageToMatrix(image)

    height = imagematrix.shape[0]
    width = imagematrix.shape[1]
    channel = imagematrix.shape[2]

    new = np.zeros((height, width, channel))

    for i in range(height):
        for j in range(width):
            for k in range(channel):
                new[i, j, k] = 255 - imagematrix[i, j, k]

    new = new / 255    
    return matrixToImages(new)


photos = loadImage('./Sierra47.jpg')

image = imageReverse(photos)
image.show()

# plt.figure('Image Zoom')
# plt.imshow(image)
# plt.show()
