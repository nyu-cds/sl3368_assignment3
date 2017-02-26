import itertools


def zbits(n, k):
	'''
		Returns a set of strings.

		Each string is a binary string of length n that contains k zero bits.

	'''

	# Make sure the inputs are correct
	if (type(n) != int) or (type(k) != int):
		raise ValueError('n and k must be integers')

	if n < k:
		raise ValueError('n must >= k')

	if (n < 0) or (k < 0):
		raise ValueError('n and k must >= 0') 


	# Create a binary string of 0s and 1s
	binary_str = '1' * (n-k) + '0' * k

	# A set of strings that is generated from binary_str after doing permutations
	string_set = {''.join(item) for item in itertools.permutations(binary_str, n)}

	return string_set



'''
	The program is correct after running the following tests.

'''
#assert zbits(4, 3) == {'0100', '0001', '0010', '1000'}
#assert zbits(4, 1) == {'0111', '1011', '1101', '1110'}
#assert zbits(5, 4) == {'00001', '00100', '01000', '10000', '00010'}

