
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


class Gray(object):
    def grayscaleValue(self, r, g, b):
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        return gray

    def grayFill(self, image):
        imagematrix = imageToMatrix(image)
        grayimage = np.zeros((imagematrix.shape[0], imagematrix.shape[1]))
        # print(imagematrix)
        # print(imagematrix[0][0][0])
        for i in range(imagematrix.shape[0]):
            for j in range(imagematrix.shape[1]):
                grayimage[i, j] = self.grayscaleValue(imagematrix[i][j][0], imagematrix[i][j][1], imagematrix[i][j][2])

        grayimage = grayimage / 255
        return matrixToImages(grayimage)


def imageBinarization(image, threshold): 
    image = Gray.grayFill(image)
    imagematrix = imageToMatrix(image)

    height = imagematrix.shape[0]
    width = imagematrix.shape[1]

    new = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            if imagematrix[i, j] > threshold:
                new[i, j] = 255
            else:
                new[i, j] = 0

    new = new / 255
    return matrixToImages(new)


photos = loadImage('../1.jpg')

Gray = Gray()
image = imageBinarization(photos, 150)
image.show()

# plt.figure('Image Zoom')
# plt.imshow(image)
# plt.show()
