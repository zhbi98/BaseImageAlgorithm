
from PIL import Image, ImageFilter
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


def laplaceSharpen(image, c):
    im = image.convert('L')
    im = im.filter(ImageFilter.GaussianBlur(radius=5))
    im = imageToMatrix(im)

    imagematrix = imageToMatrix(image)

    height = imagematrix.shape[0]
    width = imagematrix.shape[1]
    channel = imagematrix.shape[2]

    new = np.zeros((height, width, channel))
    new_ = np.zeros((height, width, channel))

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            # f(y, x) = f(y + 1, x) + f(y - 1, x) + f(y, x + 1) + f(y, x - 1) - 4 * f(y + 1, x)
            new[i, j] = im[i + 1, j] + im[i - 1, j] + im[i, j + 1] + im[i, j - 1] - 4 * im[i, j]
            new_[i, j] = imagematrix[i, j] + c * new[i, j]
            # new_[i, j] = new[i, j]

    new_ = new_ / 255    
    return matrixToImages(new_)


def sobelSharpen(image):
    image = np.array(image)
    imagematrix = np.array(image, dtype='double')

    height = imagematrix.shape[0]
    width = imagematrix.shape[1]
    channel = 3#imagematrix.shape[2]

    new = np.zeros((height, width, channel), dtype='uint16')

    # filter = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    filter = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    k = filter.shape[0]

    for i in range(height):
        for j in range(width):
            count = 0
            for n in range(pow(k, 2)):

                # k = 3, n = 0, 1, 2 ......,  8, a = -1,  0, 1,      b = -1, 0, 1
                # k = 5, n = 0, 1, 2, 3 ..., 24, a = -2, -1, 0, 1, 2

                a, b = int(n // k - (k - 1) / 2), int(n % k - 1)
                aa, bb = int(n // k), int(n % k)
                ft = filter[aa, bb]
                if i + a <= 0:
                    if j + b <= 0:
                        count += imagematrix[0,         0] * ft
                    elif j + b >= width - 1:
                        count += imagematrix[0,        -1] * ft
                    else:
                        count += imagematrix[0,     j + b] * ft
                elif i + a >= height - 1:
                    if j + b <= 0:
                        count += imagematrix[-1,        0] * ft
                    elif j + b >= width - 1:
                        count += imagematrix[-1,       -1] * ft
                    else:
                        count += imagematrix[-1,    j + b] * ft
                else:
                    if j + b <= 0:
                        count += imagematrix[i + a,     0] * ft
                    elif j + b >= width - 1:
                        count += imagematrix[i + a,    -1] * ft
                    else:
                        count += imagematrix[i + a, j + b] * ft
            new[i, j] = abs(count)
    max_ = np.max(new)
    min_ = np.min(new)

    new_ = np.zeros((height, width, channel), dtype='uint8')

    for i in range(height):
        for j in range(width):
            new_[i, j] = 255 * (new[i, j] - min_) / (max_ - min_)
            new_[i, j] = new_[i, j] + image[i, j] - 5
    
    new_ = new_ / 255    
    return matrixToImages(new_)


photos = loadImage('./16.jpg')
# image = photos.filter(ImageFilter.SHARPEN)
image = sobelSharpen(photos)
image.show()

# plt.figure('Image Sharpen')
# plt.imshow(image)
# plt.show()
