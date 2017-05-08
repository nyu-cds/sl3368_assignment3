'''
	Shixin Li (sl3368)

	05/07/2017

	Assignmnet 13 Part 1
'''

from pyspark import SparkContext
import re
import operator

# remove any non-words and split lines into separate words
# finally, convert all words to lowercase
def splitter(line):
    line = re.sub(r'^\W+|\W+$', '', line)
    return map(str.lower, re.split(r'\W+', line))

if __name__ == '__main__':
	sc = SparkContext("local", "distinct_words_count")

	text = sc.textFile('pg2701.txt')
	words = text.flatMap(splitter)
	words_mapped = words.map(lambda x: (x,1))
	sorted_map = words_mapped.sortByKey()
	
	# Count the number of distinct words in the input text.
	num_distinct = sorted_map.reduceByKey(operator.add_).count()

	print ('The number of distinct words in the input text is {}.'.format(num_distinct))