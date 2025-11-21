
# **Image processing**
 
![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg) 
[![Build Status](https://travis-ci.com/zhbi98/image.svg?branch=master)](https://travis-ci.com/zhbi98/image)

**Here mainly realizes the common image processing such as fisheye correction, Gaussian blur, transparency, saturation sharpening, gray filling, arbitrary angle rotation and so on. These algorithms are implemented from the bottom through Python, and the implementation process of each algorithm is described in detail below**

## _Ⅰ. Alpha_

The image is made up of a series of pixels, and the original colors of the image are displayed by the pixels emitting light.The color of each pixel of the image is composed of standard colors R, G and B.So when the image is processed by the algorithm, the RGB value of the pixel of the image is actually recalculated A process of recombination of calculations.

For processing the transparency of the image through the algorithm, it is actually on the original image through the algorithm Cover with a layer of colored mask. The color of the mask can be any combination of RGB.That is to say, for an image A, it is covered with a mask B, what we can seeThe image C is the image A seen through the mask B.So what we actually see is the RGB value of image C.

So what we have to do is to calculate the RGB value of image C.

#### 1.So transparency blending algorithm:

`A(C) = (1-alpha)*A(B) + alpha*A(A)` 

`R(C) = (1-alpha)*R(B) + alpha*R(A)`  
`G(C) = (1-alpha)*G(B) + alpha*G(A)`  
`B(C) = (1-alpha)*B(B) + alpha*B(A)`
 
#### [[You can also refer to](https://www.cnblogs.com/kongqiweiliang/p/3773127.html)]  

#### 2.Algorithm effect:  
_original image1_  
<img src="https://s1.ax1x.com/2020/05/10/Y3PShR.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />  
_original image2_  
<img src="https://s1.ax1x.com/2020/05/10/Y3mHIK.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />  
_original image1 monochrome mixing_  
<img src="https://s1.ax1x.com/2020/05/10/Y3n7Os.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />  
_original image1 and image2 mixing_  
<img src="https://s1.ax1x.com/2020/05/10/Y3ui01.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />  

:+1:The effect looks good!

## _Ⅱ. Binarizations_

Image binarization, as the name implies, is to convert the RGB color values of the image to 0 or 1, that is, an image is only composed of 0 and 1, in the field of electronic technology, 0 represents closed 1 represents open, for pixels 0 represents no display 1 stands for display, so the image after a binarization operation consists of only black and white. This is widely used in machine vision, because for computers, they can only process 0-1 data, and do not need to know what color the image is. They only need to know the outline of the image, so they know 0 and 1 are enough.

Before performing the binarization operation, we have to perform another operation, that is, to convert the image to a grayscale image. Why is such an operation required?
Here I will talk about the dimension of the image. For a photo, it is composed of a series of pixels, so when we want to control a certain pixel, we can communicate index through rows and columns, such as [x, y], but just x and y are not enough, why? Because x and y only describe where this pixel is Ah, it does not describe what color this pixel is. So we also need to introduce a z, use z to specify the color value, and use the color value to describe what the pixel is. colored. so there is [x, y, z], indicating that the position of this pixel is [x, y] and the color is z. so describing a pixel that constitutes a color photo needs to three-dimensional data to represent.so for a color picture it is a three-dimensional data matrix.therefore, the picture is processed into gray, which can reduce the color dimension of the image.

#### Gray filling algorithm:  

`gray = 0.299 * r + 0.587 * g + 0.114 * b`  

>This is a psychological formula, but it can also be used to process the image into gray, which is interesting,
r, g, b Indicates how many standard red, green, and blue pixels each make up of the original image pixels.

_original image_  
<img src="https://s1.ax1x.com/2020/05/10/Y3PShR.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />  
_Look, this is how it looks_  
<img src="https://s1.ax1x.com/2020/05/10/Y3YKGn.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />  

After the image is processed into gray, there is no color, which means R = G = B = gray, so the color dimension of the color photo is also reduced, so this is also similar to a proportional mixing, mixing RGB values of color photos in a ratio of 0.299: 0.587: 0.114
Ok, everything is very easy to handle. After the color is processed into gray, only the dark and light colors are left for the color of the image. At this time, we can set a threshold to assign pixels with a color depth greater than the threshold 255 makes it appear white, and assign a value of 0 where it is smaller than the threshold to make it appear black. The color value is either 0 or 255, which is very good. the original color image is only black and white in a blink of an eye.  

```
if imagematrix[i, j] > threshold:
    new[i, j] = 255
else:
    new[i, j] = 0
```

You think that's fine, I said earlier that in computer image recognition, the computer only knows 0 and 1, but now the data values in the image matrix are 0 and 255, so don't worry, we will put each data of the image The value is divided by 255, so that the value of the image matrix is processed into 0 and 1.
_Okay, let's see the effect now_  
<img src="https://s1.ax1x.com/2020/05/10/Y3dWK1.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />

## _Ⅲ. Gauassian bar_

Blur is widely used in UI special effects, such as iOS, Android, MIUI, Windows operating system. of course, blur also plays an important role in image filters, and Gaussian blur is the most widely used in blur algorithms. gaussian blur is mainly named after the mathematician Gaussian. Gaussian blur mainly uses Gaussian distribution [normal distribution] for image blur processing. let us carefully analyze the implementation process of Gaussian blur algorithm.  

#### 1. Gaussian fuzzy principle:  

The so-called "blur" can be understood as the average value of surrounding pixels for each pixel.  
<img src="https://s1.ax1x.com/2020/05/12/YUuH0S.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />  <img src="https://s1.ax1x.com/2020/05/12/YUKG9A.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />  

**This is the effect,  the average value of the surrounding points will be 1**

When calculating the average value, the larger the range of surrounding pixels, the stronger the blur effect

<img src="https://s1.ax1x.com/2020/05/12/YUQAQ1.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />  <img src="https://s1.ax1x.com/2020/05/12/YUQmdO.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />  <img src="https://s1.ax1x.com/2020/05/12/YUQQWd.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />  

#### 2. Normally distributed weights:

###### _2.1 one dimensional normal distribution_

<img src="https://s1.ax1x.com/2020/05/12/YU1lrt.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />  
For the value through the relationship, the normal distribution is obviously a desirable weight distribution mode. on the graph, the normal distribution is a bell-shaped curve, the closer to the center, the larger the value, the farther from the center, the smaller the value.  
When calculating the average value, we only need to use the "center point" as the origin, and assign weights to other points according to their positions on the normal curve, and we can get a weighted average.

For the above normal distribution image is one-dimensional, but for an image, it is a plane with rows and columns, so we need a two-dimensional normal distribution image

###### _2.2 two dimensional normal distribution_

<img src="https://s1.ax1x.com/2020/05/12/YUtiKH.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />  

#### 3. Gaussian function:

###### _3.1 One-dimensional Gaussian function_    

<img src="https://s1.ax1x.com/2020/05/13/YawtyT.jpg" alt="GitHub" title="GitHub,Social Coding" width="300" height="60" /> 
Where μ is the mean of x and σ is the variance of x. Since the center point is the origin when calculating the average value, μ is equal to 0.  
So the following formula:   
<img src="https://s1.ax1x.com/2020/05/13/Ya0huT.jpg" alt="GitHub" title="GitHub,Social Coding" width="300" height="60" />  

###### _3.2 Two-dimensional Gaussian function_

According to the one-dimensional Gaussian function, the two-dimensional Gaussian function can be derived
<img src="https://s1.ax1x.com/2020/05/13/YaBrM6.jpg" alt="GitHub" title="GitHub,Social Coding" width="300" height="60" /> 
Well, with this two-dimensional Gaussian function we can proceed to the next operation

#### 4. Weight matrix:

Assuming the coordinates of the center point are [0, 0], then the coordinates of the 8 points closest to it are as follows:   
<img src="https://s1.ax1x.com/2020/05/13/Ydrx0K.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />  

Now we need to calculate the weight matrix. In order to calculate the weight matrix, we need to set the value of σ. Assuming σ = 1.5, the weight matrix with a blur radius of 1 is as follows:   
<img src="https://s1.ax1x.com/2020/05/13/YdyOZ6.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />  

The sum of the weights of these 9 points is equal to 0.4787147. If only the weighted average of these 9 points is calculated, the sum of their weights must be equal to 1. Therefore, the above 9 values must be divided by 0.4787147 to obtain the final weight matrix.   
<img src="https://s1.ax1x.com/2020/05/13/Yd6PsI.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />  

#### 5. Calculate Gaussian Blur:  

The weight matrix is calculated, now we can calculate the Gaussian fuzzy value we need.  
If we now have 9 pixels, the value range is 0 to 255, and their values are as shown in the figure below.
<img src="https://s1.ax1x.com/2020/05/24/tSbIk6.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />    
Now we multiply these pixels by their respective weight values, and their weight values are as follows.  
<img src="https://s1.ax1x.com/2020/05/24/tSbv7t.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />    
Then you get the value shown in the figure below.  
<img src="https://s1.ax1x.com/2020/05/24/tSqAns.jpg" alt="GitHub" title="GitHub,Social Coding" width="200" height="162" />    
Nine values are obtained here, and the calculated nine values are added together to obtain the color value of the center pixel. We repeat the above calculation and take values for all pixels of the image to obtain a Gaussian blurred image Too.    

_Okay, let ’s take a look at the effect_  
_original image_    
<img src="https://s1.ax1x.com/2020/05/24/tSL7sH.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" />   
_After processing_    
<img src="https://s1.ax1x.com/2020/05/24/tSL0iV.jpg" alt="GitHub" title="GitHub,Social Coding" width="600" height="338" /> 
