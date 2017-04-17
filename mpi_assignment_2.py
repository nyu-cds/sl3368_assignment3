'''
	Shixin Li (sl3368)

	04/16/2017

	Assignment 10 part 2:
		1. Process 0 reads a value from the user and verifies that it is an integer less than 100.
		2. Process 0 sends the value to process 1 which multiplies it by its rank.
		3. Process 1 sends the new value to process 2 which multiplies it by its rank.
		4. This continues for each process, such that process i sends the value to process i+1 which multiplies it by i+1.
		5. The last process sends the value back to process 0, which prints the result.
'''

import numpy as np 
from mpi4py import MPI 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

randNum = np.zeros(1, dtype=int)

## Check the number of process.
if size < 2:
	raise ValueError ('Need 2 or more processes')

if rank == 0:
	while True:
		print ('Please enter an integer less than 100: ')
		input_value = raw_input()
		## Check if input is an integer.
		try:
			input_value = int(input_value)
		except ValueError:
			print ('This is not an integer, please enter a valid integer!\n')
			continue
		## Check if input is less than 100.
		else:
			if input_value >= 100:
				print ('Error! This integer is not less than 100!\n')
				continue
			else:
				break

	randNum[0] = input_value
	print ('\nProcess %d reads the initial value is %d' % (rank, randNum[0]))
	comm.Send(randNum, dest=1)
	comm.Recv(randNum, source=size-1)
	print ('\nProcess %d receives the final value and the value is %d' % (rank, randNum[0]))

if 0 < rank < size-1:
	comm.Recv(randNum, source=rank-1)
	randNum *= rank
	comm.Send(randNum, dest=rank+1)

## Check if it is the last process.
if rank == size-1:
	comm.Recv(randNum, source=rank-1)
	randNum *= rank
	## Send the value back to the process 0.
	print ('\nThe rank of the last process is %d' % rank)
	comm.Send(randNum, dest=0)

