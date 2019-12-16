import os
import sys
from pyspark.sql import SparkSession
from operator import add

wordsList = ['cat', 'ele', 'rat', 'rat', 'cat']
wordsRDD = sc.parallelize(wordsList)

print(sorted(wordsRDD.map(lambda x: (x,1)).reduceByKey(add).collect(), reverse=True))

