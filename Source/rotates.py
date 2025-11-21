
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
        # after rotation image width_
        # after rotation image height_
        # after rotation image coordinate x0
        # after rotation image coordinate y0
        # after rotation math coordinate x
        # after rotation math coordinate y
        # x = x0 - 0.5 * width_
        # y = -y0 + 0.5 * height_
    def toMathCoordinate(self, x0, y0, width_, height_):
        x = x0 - 0.5 * width_
        y = -y0 + 0.5 * height_
        
        return x, y

        # [a] rotation angle
        # x_ = x * cos(a) - y * sin(a)
        # y_ = x * sin(a) + y * cos(a)
         
        # x = x_ * cos(a) + y_ * sin(a)
        # y = y_ * cos(a) - x_ * sin(a)
    def rotationAngle(self, x_, y_, angle):
        # a known unrotated x, y find out after rotation x_, y_
        # x_ = x * math.cos(self.angle) - y * math.sin(self.angle)
        # y_ = x * math.sin(self.angle) + y * math.cos(self.angle)
        
        # a known after rotation x_, y_ find out unrotated x, y
        x = x_ * math.cos(self.angle) + y_ * math.sin(self.angle)
        y = y_ * math.cos(self.angle) - x_ * math.sin(self.angle)

        return x, y

        # math coordinate -> image coordinate
        # original image width
        # original image height
        # x0 = x + 0.5 * width
        # y0 = -y + 0.5 * height
        # unrotated image coordinate x0
        # unrotated image coordinate y0
        # unrotated math coordinate x
        # unrotated math coordinate y
    def toImageCoordinate(self, x, y, width, height):
        x0 = x + 0.5 * width
        y0 = -y + 0.5 * height
        
        return x0, y0

    def originalPos(self, x0, y0, width_, height_, width, height):
        mathx_, mathy_ = self.toMathCoordinate(x0, y0, width_, height_)
        
        mathx, mathy = self.rotationAngle(mathx_, mathy_, self.angle)
        
        x0, y0 = self.toImageCoordinate(mathx, mathy, width, height)

        return int(x0), int(y0)

    def rotateImage(self, image):
        imagematrix = imageToMatrix(image)

        height = imagematrix.shape[0]
        width = imagematrix.shape[1]
        channel = imagematrix.shape[2]

        newwidth = int(width * abs(math.cos(self.angle)) + height * abs(math.sin(self.angle))) + 1
        newheight = int(width * abs(math.sin(self.angle)) + height * abs(math.cos(self.angle))) + 1

        new = np.zeros((newheight, newwidth, channel))

        # Fill the matrix with white
        # for i in range(newheight):
        #     for j in range(newwidth):
        #         new[i, j] = 255 
        
        for i in range(newheight):
            for j in range(newwidth):
                x, y = self.originalPos(j, i, newwidth, newheight, width, height)
                
                # x * y > 0 
                # Because the image coordinate axis has 
                # only positive quadrants, ensure that 
                # the negative quadrant of the coordinate 
                # system does not appear in the image 
                # coordinates
                if x < width and y < height and x * y > 0:
                    new[i, j] = imagematrix[y, x]

        new = new / 255    
        return matrixToImages(new)


photos = loadImage('./16.jpg')

ImageRotate = ImageRotate(angle=30)
image = ImageRotate.rotateImage(photos)
image.show()

# plt.figure('Image Zoom')
# plt.imshow(image)
# plt.show()
