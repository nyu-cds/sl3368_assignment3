'''
	Shixin Li (sl3368)

	05/07/2017

	Assignmnet 13 Part 3
'''

from pyspark import SparkContext
from operator import add
import math

if __name__ == '__main__':
	sc = SparkContext("local", "squareroot")
	# Create an RDD of numbers from 1 to 1000.
	nums = sc.parallelize(range(1, 1001))
	# Compute square roots.
	squareroots = nums.map(math.sqrt)
	# Calculate the average of the square roots.
	avg_sqrt = squareroots.fold(0, add)/float(1000)
	print ('The average of the square root of all the numbers from 1 to 1000 is {}.'.format(avg_sqrt))
