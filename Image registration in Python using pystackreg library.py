# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 17:26:58 2021

@author: abc
"""

"""

Image registration using pystackreg library using Python


"""

from pystackreg import StackReg
from skimage import io
from matplotlib import pyplot as plt

#Read our images
ref_img = io.imread("for_alignment/shale_for_alignment00.tif")
offset_img = io.imread("for_alignment/shale_for_alignment01.tif")

#Let's begin process of image registration using pystackreg library

#Translation transformation
sr = StackReg(StackReg.TRANSLATION)
out_tra = sr.register_transform(ref_img, offset_img)

#Rigid body transformation
sr = StackReg(StackReg.RIGID_BODY)
out_rot = sr.register_transform(ref_img, offset_img)

#Scaled Rotation transformation
#sr = StackReg(StackReg.SCALED_ROTATION)
#out_sca = sr.register_transform(ref_img, offset_img)

#Affline transformation
sr = StackReg(StackReg.AFFINE)
out_aff = sr.register_transform(ref_img, offset_img)

#Bilinear transformation
#sr = StackReg(StackReg.BILINEAR)
#out_bil = sr.register_transform(ref_img, offset_img)

#Let's plot all the images
from matplotlib import pyplot as plt
fig = plt.figure(figsize=(10, 10))
ax1 = fig.add_subplot(2,2,1)
ax1.imshow(ref_img, cmap='gray')
ax1.title.set_text('Input image')
ax2 = fig.add_subplot(2,2,2)
ax2.imshow(out_tra, cmap='gray')
ax2.title.set_text('Translation transformation')
ax3 = fig.add_subplot(2,2,3)
ax3.imshow(out_rot, cmap='gray')
ax3.title.set_text('Rigid body transformation')
ax4 = fig.add_subplot(2,2,4)
ax4.imshow(out_aff, cmap='gray')
ax4.title.set_text('Affine transformation')
plt.show()

#After the execution of above I realize that single image does't make sense for this example.
#So Let us look at the stack for multiple images

##############################################################################

#Let's create a tiff stack image from individual images

import glob
import tifffile

with tifffile.TiffWriter('my_image_stack.tif') as stack:
    for filename in glob.glob('for_alignment/*.tif'):
        stack.save(tifffile.imread(filename))


#Let's register and transform a whole stack

from pystackreg import StackReg
from skimage import io

#Read our image
img0 = io.imread('my_image_stack.tif')

#Apply Rigid body transformation
sr = StackReg(StackReg.RIGID_BODY)

#Register each frame to the previous one that already registered
#this is what the originaL StackReg ImageJ plugin uses
out_previous = sr.register_transform_stack(img0, reference='previous')

#To save the output to a tiff stack image
#First convert float values to int
import numpy
out_previous_int = out_previous.astype(numpy.int8)

#Using tifffile to save the stack into a single tif
import tifffile
tifffile.imsave('my_aligned_stack.tif', out_previous_int)

#Register to first image
out_first = sr.register_transform_stack(img0 , reference='first')

#Register to mean image
out_mean = sr.register_transform_stack(img0, reference='mean')

#register to mean of first 10 images
out_first10 = sr.register_transform_stack(img0, reference='first', n_frames=1)

#Calculate a moving average of 10 images , then register the moving average images
#the first 10 images and transform the original image (not the moving average image)
out_moving10 = sr.register_transform_stack(img0, reference='first', n_frames=1)



























































