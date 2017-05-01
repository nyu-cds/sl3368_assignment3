'''
	Shixin Li (sl3368)

	04/30/2017
	
	Assignment 12
'''
# 
# A CUDA version to calculate the Mandelbrot set
#
from numba import cuda
import numpy as np
from pylab import imshow, show
import math

@cuda.jit(device=True)
def mandel(x, y, max_iters):
	'''
	Given the real and imaginary parts of a complex number,
	determine if it is a candidate for membership in the 
	Mandelbrot set given a fixed number of iterations.
	'''
	c = complex(x, y)
	z = 0.0j
	for i in range(max_iters):
		z = z*z + c
		if (z.real*z.real + z.imag*z.imag) >= 4:
			return i

	return max_iters

@cuda.jit
def compute_mandel(min_x, max_x, min_y, max_y, image, iters):
	'''
	1. Divides the image into different blocks.
	2. Each block will have a thread.
	3. Plots the image in each thread.
	'''

	# Obtain the starting x and y coordinates.
	y, x = cuda.grid(2) 

	# Get the number of threads in x, y directions. 
	x_threads = cuda.blockDim.y * cuda.gridDim.y
	y_threads = cuda.blockDim.x * cuda.gridDim.x

	height = image.shape[0]
	width = image.shape[1]
	
	pixel_size_x = (max_x - min_x) / width
	pixel_size_y = (max_y - min_y) / height

	# Get how many points should be calculated in each thread.
	x_ceil = int(math.ceil(width/float(x_threads)))
	y_ceil = int(math.ceil(height/float(y_threads)))

	# Plot in each thread.
	x_list = []
	y_list = []

	for i in range(x_ceil):
		x_list.append(x_threads*i + x)
	for i in range(y_ceil):
		y_list.append(y_threads*i + y)

	for x in x_list:
		real = min_x + x * pixel_size_x
		for y in y_list:
			imag = min_y + y * pixel_size_y
			if y < height and x < width:
				image[y, x] = mandel(real, imag, iters)

if __name__ == '__main__':
	image = np.zeros((1024, 1536), dtype = np.uint8)
	blockdim = (32, 8)
	griddim = (32, 16)
	
	image_global_mem = cuda.to_device(image)
	compute_mandel[griddim, blockdim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 20) 
	image_global_mem.copy_to_host()
	imshow(image)
	show()