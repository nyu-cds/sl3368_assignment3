'''
	Shixin Li (sl3368)

	04/23/2017

	Assignment 11
'''

import unittest
from parallel_sorter import *


class Test(unittest.TestCase):

	def setUp(self):
		pass

	## Test wheter the number we enter is the length of the dataset or not.
	##  Enter 10000 to test
	def test_generate_dataset(self):
		unsorted_dataset = generate_dataset()
		self.assertEqual(len(unsorted_dataset), 10000)
		self.assertTrue(max(unsorted_dataset) < 10000)


if __name__ == '__main__':
	unittest.main()

