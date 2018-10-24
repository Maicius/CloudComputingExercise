from __future__ import print_function
from pyspark import SparkContext as sc
from pyspark import SparkConf
import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

conf = SparkConf().setAppName("miniProject").setMaster("local[*]")


def input_and_ouput():
    # lines = ssc.textFileStream('hdfs://localhost:9000/user/chikuo/')
    lines = ssc.textFileStream('file:///Users/chikuo/PycharmProjects/CloudComputing/nihao/')
    words = lines.flatMap(lambda line: line.split(' '))
    wordCounts = words
    wordCounts.pprint()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: network_wordcount.py <hostname> <port>", file=sys.stderr)
        exit(-1)
    sc = sc.getOrCreate(conf)
    ssc = StreamingContext(sc, 3)
    input_and_ouput()
    ssc.start()
    ssc.awaitTermination()
