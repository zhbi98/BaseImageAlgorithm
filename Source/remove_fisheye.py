
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

            srcy = int(srcy + height / 2)
            srcx = int(srcx + width / 2)

            new[i, j] = imagematrix[srcy, srcx]

    new = new / 255
    return matrixToImages(new)


photos = loadImage('./22.jpg')

image = removeFishEye(photos, 2)
image.show()

# plt.figure('Remove Fish Eye')
# plt.imshow(image)
# plt.show()
