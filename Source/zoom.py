
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


def zoomPhotos(image, ratio):
    img = imageToMatrix(image)
    print(img)
    height = (int)(img.shape[0] * ratio)
    width = (int)(img.shape[1] * ratio)
    channel = img.shape[2]
    new = np.zeros((height, width, channel))
    
    for i in range(height):
        for j in range(width):
            for k in range(channel):
                srcx = (i + 0.5) / ratio - 0.5
                srcy = (j + 0.5) / ratio - 0.5
     
                srcx = int(srcx)
                srcy = int(srcy)
                new[i, j, k] = img[srcx, srcy, k]
    
    new = new / 255
    return matrixToImages(new)


def zoomPhotosPlus(image, ratio):
    img = imageToMatrix(image)
    height = (int)(img.shape[0] * ratio)
    width = (int)(img.shape[1] * ratio)
    channel = img.shape[2]
    new = np.zeros((height, width, channel))
 
    for i in range(height):
        for j in range(width):
            for k in range(channel):
                srcx = (i + 0.5) / ratio - 0.5
                srcy = (j + 0.5) / ratio - 0.5
     
                intx = int(srcx)
                floatx = srcx - intx
     
                inty = int(srcy)
                floaty = srcy - inty
     
                if intx == img.shape[0] - 1:
                    intx_p = img.shape[0] - 1
                else:
                    intx_p = intx +  1
     
                if inty == img.shape[1] - 1:
                    inty_p = img.shape[1] - 1
                else:
                    inty_p = inty + 1
                
                # f(i+u, j+v) = (1-u) * (1-v) * f(i, j) + u * (1-v) * f(i+1, j) + (1-u) * v * f(i, j+1) + u * v * f(i+1, j+1)
                new[i, j, k] = (1 - floatx) * (1 - floaty) * img[intx, inty, k] + (1 - floatx) * floaty * img[intx, inty_p, k] + floatx * (1 - floaty) * img[intx_p, inty, k] + floatx * floaty * img[intx_p, inty_p, k]
                
                if (i % 500 == 0) and (j % 100 == 0):
                    print("zoom photos")

    new = new / 255
    return matrixToImages(new)


photos = loadImage('./16.jpg')

image = zoomPhotosPlus(photos, 1000)
image.show()

# plt.figure('Image Zoom')
# plt.imshow(image)
# plt.show()
