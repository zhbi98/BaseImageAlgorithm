
from PIL import Image

import math
import numpy as np
import matplotlib.pyplot as plt


# Image load
# image = Image.open('./Sierra22.jpg')
# image.show()
# print(image)

# matplot load
# image = plt.imread('./Sierra22.jpg')
# plt.imshow(image)


def loadImage(path):
    image = Image.open(path)
    return image


def imageToMatrix(image):
    matrix = np.asarray(image)
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


class ImageRotate(object):
    def __init__(self, angle=90):
        self.angle = angle * math.pi / 180

        # image coordinate -> math coordinate
        # image width
        # image height
        # x = x0 - 0.5 * width
        # y = -y0 + 0.5 * height
    def toMathCoordinate(self, x0, y0, width, height):
        x = x0 - 0.5 * width
        y = -y0 + 0.5 * height
        
        return x, y

        # [a] rotation angle
        # x_ = x * cos(a) - y * sin(a)
        # y_ = x * sin(a) + y * cos(a)
    def rotationAngle(self, x, y, angle):
        x_ = x * math.cos(self.angle) - y * math.sin(self.angle)

        y_ = x * math.sin(self.angle) + y * math.cos(self.angle)

        return x_, y_

        # math coordinate -> image coordinate
        # new image width_
        # new image height_
        # x0 = x + 0.5 * width_
        # y0 = -y + 0.5 * height_
    def toImageCoordinate(self, x, y, width_, height_):
        x0 = x + 0.5 * width_
        y0 = -y + 0.5 * height_
        
        return x0, y0

    def newPos(self, x0, y0, width, height, width_, height_):
        mathx, mathy = self.toMathCoordinate(x0, y0, width, height)
        
        mathx_, mathy_ = self.rotationAngle(mathx, mathy, self.angle)
        
        x0, y0 = self.toImageCoordinate(mathx_, mathy_, width_, height_)

        return int(x0), int(y0)

    def rotateImage(self, image):
        imagematrix = imageToMatrix(image)

        height = imagematrix.shape[0]
        width = imagematrix.shape[1]
        channel = imagematrix.shape[2]

        newwidth = int(width * abs(math.cos(self.angle)) + height * abs(math.sin(self.angle))) + 1
        newheight = int(width * abs(math.sin(self.angle)) + height * abs(math.cos(self.angle))) + 1

        new = np.zeros((newheight, newwidth, channel))
        
        for i in range(height):
            for j in range(width):
                x, y = self.newPos(j, i, width, height, newwidth, newheight)
                new[y, x] = imagematrix[i, j]

        new = new / 255    
        return matrixToImages(new)


photos = loadImage('./13.jpg')

ImageRotate = ImageRotate(angle=90)
image = ImageRotate.rotateImage(photos)
image.show()

# plt.figure('Image Zoom')
# plt.imshow(image)
# plt.show()
