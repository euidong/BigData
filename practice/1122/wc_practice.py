import sys
import re
from operator import add

from pyspark import SparkContext

def map_phase(x):
		x = re.sub('--', ' ', x)
		x = re.sub("'", '', x)
		return re.sub('[?!@#$\'",.;:()]', '', x).lower()

if __name__ == "__main__":
	if len(sys.argv) < 4:
  	  print >> sys.stderr, "Usage: wordcount <master> <inputfile> <outputfile>"
  	  exit(-1)
	sc = SparkContext(sys.argv[1], "python_wordcount_sorted in bigdataprogrammiing")
	lines = sc.textFile(sys.argv[2], 2)
	print(lines.getNumPartitions()) # print the number of partitions
	lines = lines.map(lambda x:map_phase(x))
	lines = lines.filter(lambda x: x!="neighborhood")
	notTokyo = lines.filter(lambda x: x!="tokyo")
	count = notTokyo.map(lambda x: (x,1)).reduceByKey(lambda x,y : x+y)
	outRDD = count.map(lambda x: (x[0].encode("utf-8", "ignore"), x[1]))
	outRDD = outRDD.sortByKey(True)
	outRDD.saveAsTextFile(sys.argv[3])
	
