from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import time

class HDFSStreaming(object):
    def __init__(self):
        conf = SparkConf().setAppName("SparkTopK").setMaster("local[*]")
        self.sc = SparkContext.getOrCreate(conf)
        self.streamContext = StreamingContext(self.sc, 2)
        self.dataDirectory = "hdfs://localhost:9000/user/maicius/test_data/"
        self.streamContext.textFileStream(self.dataDirectory)

    def save_data_to_hdfs(self):
        i = 0
        for i in range(100):
            data = [1, 2]

            rdd = self.sc.parallelize(data)
            rdd.map(lambda x: x + i)
            print(data)
            print(i)
            rdd.saveAsTextFile(self.dataDirectory + str(i) + ".txt")
            time.sleep(1)


if __name__ == '__main__':
    hdfs = HDFSStreaming()
    hdfs.save_data_to_hdfs()



