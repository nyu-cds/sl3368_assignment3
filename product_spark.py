'''
	Shixin Li (sl3368)

	05/07/2017

	Assignmnet 13 Part 2
'''

from pyspark import SparkContext
from operator import mul

if __name__ == '__main__':
	sc = SparkContext("local", "product")
	# Create an RDD of numbers from 1 to 1000.
	nums = sc.parallelize(range(1, 1001))
	# Compute the product of all the numbers from 1 to 1000 
	product = nums.fold(1, mul)

	print ('The product of all the numbers from 1 to 1000 is {}.'.format(product))
