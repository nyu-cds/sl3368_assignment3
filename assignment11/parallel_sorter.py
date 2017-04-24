'''
	Shixin Li (sl3368)

	04/23/2017

	Assignment 11
'''

import numpy as np
from mpi4py import MPI 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

## Check the number of process.
if size < 1:
	raise ValueError ('Need at least 1 process')

## Function used to generate an unsorted dataset.
def generate_dataset():
	while True:
		print ('Please enter the number of elements in the dataset (a large integer around 10000): ')
		num_elements = raw_input()
		## Check if input is an integer.
		try:
			num_elements = int(num_elements)
		except ValueError:
			print ('This is not an integer, please enter a valid integer!\n')
			continue
		## Check if input is less than 500.
		else:
			if num_elements < 500:
				print ('Error! This integer is too small. Please enter a larger one!\n')
				continue
			else:
				break

	## Generate a dataset
	unsorted_dataset = np.random.randint(low = 0, high = num_elements, size = num_elements)

	return unsorted_dataset


def parallel_sort():
	'''
		This function first slices the dataset, then sends the sub datasets to each of the process to sort, and
		finally sends sorted sub datasets back to the root process (process with rank = 0) and reunify them.
	'''
	if rank == 0:
		unsorted_dataset = generate_dataset()
		print ('\nProcess 0 generates an initial unsorted dataset: {}'.format(unsorted_dataset))

		# Slice the initial dataset
		sub_unsorted_dataset = []
		bin = np.array_split(np.asarray(range(min(unsorted_dataset), max(unsorted_dataset)+1)), size)
		for i in range(size):
			sub_unsorted_dataset.append([value for value in unsorted_dataset if (value in bin[i])])

	else:
		sub_unsorted_dataset = None

	## Send bins to processes. 
	data_to_send = comm.scatter(sub_unsorted_dataset, root = 0)
	## Sort the data
	sub_sorted_dataset = np.sort(data_to_send)
	## Gather the data
	data_to_gather = comm.gather(sub_sorted_dataset, root = 0)

	## Concatenate sorted data
	if rank == 0:
		sorted_dataset = np.concatenate(data_to_gather)
		print ('\nFinal sorted dataset is:')
		print sorted_dataset


if __name__ == '__main__':
	parallel_sort()

