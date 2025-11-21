
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


class ImageSaturation(object):
    def __init__(self, satur=0.5):
        self.satur = satur

    def rgbToHsl(self, imagematrix):
        rgbmin = imagematrix.min(axis=2)
        rgbmax = imagematrix.max(axis=2)

        # s represents saturation, 
        # min and max represent the
        # minimum and maximum values
        # of R, G, and B color values
        # in RGB space, and the range
        # is a real number of 0-1, so
        # dividing by 255.0 converts
        # RGB from 0 - 255 to 0 - 1
        delta = (rgbmax - rgbmin) / 255.0
        value = (rgbmax + rgbmin) / 255.0
        # l = 1/2 * (max + min)
        l = value / 2.0

        return delta, value, l

    def hslS(self, delta, value, l):
        # s = (max - min) / (max + min)       when(l<1/2)
        _s = delta / (value + 0.001)
        # s = (max - min) / (2 - (max - min)) when(l>1/2)
        s_ = delta / (2 - (value + 0.001))

        s = _s * l + s_ * (1 - l)

        return s

    def imageSaturation(self, image):
        imagematrix = imageToMatrix(image)

        imagematrix = imagematrix * 1.0

        height = imagematrix.shape[0]
        width = imagematrix.shape[1]
        channel = imagematrix.shape[2]

        new = np.zeros((height, width, channel))
        new = imagematrix * 1.0

        delta, value, l = self.rgbToHsl(imagematrix)
        s = self.hslS(delta, value, l)

        _mask = l < 0.5

        if self.satur >= 0:
            temp = self.satur + s
            mask_ = temp >  1
            
            _alpha = s
            alpha_ = s * 0 + 1 - self.satur
            alpha = _alpha * mask_ + alpha_ * (1 - mask_)
            alpha = 1 / (alpha + 0.001) - 1

            new[:, :, 0] = imagematrix[:, :, 0] + (imagematrix[:, :, 0] - l * 255.0) * alpha
            new[:, :, 1] = imagematrix[:, :, 1] + (imagematrix[:, :, 1] - l * 255.0) * alpha
            new[:, :, 2] = imagematrix[:, :, 2] + (imagematrix[:, :, 2] - l * 255.0) * alpha

        else:
            alpha = self.satur
            new[:, :, 0] = l * 255.0 + (imagematrix[:, :, 0] - l * 255.0) * (1 + alpha)
            new[:, :, 1] = l * 255.0 + (imagematrix[:, :, 1] - l * 255.0) * (1 + alpha)
            new[:, :, 2] = l * 255.0 + (imagematrix[:, :, 2] - l * 255.0) * (1 + alpha)

        new = new / 255

        _mask = new  < 0
        mask_ = new  > 1

        new = new * (1 - _mask)
        new = new * (1 - mask_) + mask_

        return matrixToImages(new)


photos = loadImage('./13.jpg')

ImageSaturation = ImageSaturation(-0.2)
image = ImageSaturation.imageSaturation(photos)
image.show()

# plt.figure('Image Zoom')
# plt.imshow(image)
# plt.show()
