
from PIL import Image
from PIL import ImageTk

import math
import numpy as np
import matplotlib.pyplot as plt


# Image load
# image = Image.open('./Sierra16.jpg')
# image.show()
# print(image)

# matplot load
# image = plt.imread('./Sierra16.jpg')
# plt.imshow(image)


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


# A(C) = (1-alpha)*A(B) + alpha*A(A)

# R(C) = (1-alpha)*R(B) + alpha*R(A)
# G(C) = (1-alpha)*G(B) + alpha*G(A)
# B(C) = (1-alpha)*B(B) + alpha*B(A)
class ImageAlpha(object):
    def __init__(self, alpha=0.5, mixr=0, mixg=0, mixb=0):
        self.alpha = alpha
        self.mixr = mixr;
        self.mixg = mixg;
        self.mixb = mixb;

    def rgbMixing(self, r, g, b):
        targetr = (1 - self.alpha) * self.mixr + self.alpha * r
        targetg = (1 - self.alpha) * self.mixg + self.alpha * g
        targetb = (1 - self.alpha) * self.mixb + self.alpha * b

        return targetr, targetg, targetb

    def mixingImage(self, image):
        imagematrix = imageToMatrix(image)

        height = imagematrix.shape[0]
        width = imagematrix.shape[1]
        channel = imagematrix.shape[2]
        new = np.zeros((height, width, channel))

        for i in range(height):
            for j in range(width):
                # for k in range(channel):
                new[i, j] = self.rgbMixing(imagematrix[i][j][0], imagematrix[i][j][1], imagematrix[i][j][2])

        new = new / 255
        return matrixToImages(new)


class ImageMixing(object):
    def __init__(self, alpha=0.5):
        self.alpha = alpha

    def rgbMixing(self, mixr, mixg, mixb, r, g, b):
        mixrs = (1 - self.alpha) * mixr + self.alpha * r
        mixgs = (1 - self.alpha) * mixg + self.alpha * g
        mixbs = (1 - self.alpha) * mixb + self.alpha * b

        return mixrs, mixgs, mixbs

    def mixingImage(self, image, _image):
        imagematrix = imageToMatrix(image)
        _imagematrix = imageToMatrix(_image)

        height = imagematrix.shape[0]
        width = imagematrix.shape[1]
        channel = imagematrix.shape[2]
        new = np.zeros((height, width, channel))

        for i in range(height):
            for j in range(width):
                for k in range(channel):
                    new[i, j] = self.rgbMixing(imagematrix[i][j][0], imagematrix[i][j][1], imagematrix[i][j][2], _imagematrix[i][j][0], _imagematrix[i][j][1], _imagematrix[i][j][2])
        
        new = new / 255
        return matrixToImages(new)


photos = loadImage('./Sierra17.jpg')
photos2 = loadImage('./Sierra18.jpg')
# ImageAlpha = ImageAlpha(alpha=0.2, mixr=0, mixg=0, mixb=0)
# image = ImageAlpha.mixingImage(photos)
# image.show()

ImageMixing = ImageMixing(alpha=0.6)
image = ImageMixing.mixingImage(photos, photos2)
image.show()

# plt.figure('Image Alpha')
# plt.imshow(image)
# plt.show()
