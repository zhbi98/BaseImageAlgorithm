
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


def power(value, n):
    result = 1

    if n == 0:
        result = 1
    else:
        for i in range(n):
            result = result * value
    
    return result


class GaussianBlur(object):
    def __init__(self, radius=1, sigema=1.5):
        self.radius = radius
        self.sigema = sigema

    def gaussianFunction(self, x, y):
        # sigema * sigema
        sigema2 = power(self.sigema, 2)
        x2 = power(x, 2)
        y2 = power(y, 2)
        _res = 1 / (2 * math.pi * sigema2)
        res_ = math.exp(-(x2 + y2) / (2 * sigema2))
        res = _res * res_
        return res

    def filtering(self):
        siderange = self.radius * 2 + 1
        weightarray = np.zeros((siderange, siderange))
        for i in range(siderange):
            for j in range(siderange):
                weightarray[i, j] = self.gaussianFunction(i - self.radius, j - self.radius)
        
        total = np.sum(weightarray)
        weightarray = weightarray / total
        return weightarray

    def filter(self, image, weight):
        arrary = imageToMatrix(image)
        new = np.zeros(arrary.shape)

        for i in range(arrary.shape[0] - self.radius * 2):
            for j in range(arrary.shape[1] - self.radius * 2):
                for k in range(3):
                    a = np.multiply(weight, arrary[i:(i + 2 * self.radius + 1), j:(j + 2 * self.radius + 1), k])
                    new[i + self.radius, j + self.radius, k] = a.sum()

        new = new / 255
        return matrixToImages(new)


photos = loadImage('./Sierra18.jpg')

GaussianBlur = GaussianBlur(radius=5, sigema=25)
fite = GaussianBlur.filtering()

photo = GaussianBlur.filter(photos, fite)
photo.show()

# plt.figure('Gaussian Blur')
# plt.imshow(photo)
# plt.show()
