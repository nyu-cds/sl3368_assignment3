from mpi4py import MPI

comm = MPI.COMM_WORLD
## Get the rank of the process.
rank = comm.Get_rank()

## Check if it is even rank.
if rank % 2 == 0:
	print ('Hello from process %d' % rank)

## Check if it is odd rank.
if rank % 2 == 1:
	print ('Goodbye from process %d' % rank)
