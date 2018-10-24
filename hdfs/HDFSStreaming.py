from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
import time
from jedis.jedis import jedis
import json

class HDFSStreaming(object):
    def __init__(self):
        conf = SparkConf().setAppName("SparkStreamingSaving").setMaster("local[*]")
        self.sc = SparkContext.getOrCreate(conf)
        self.dataDirectory = "hdfs://localhost:9000/user/maicius/test_data/"

        self.redis = jedis()

    def save_data_to_hdfs(self, data, file_name):

        rdd = self.sc.parallelize(data)
        rdd = rdd.map(lambda x: x.replace("\'", "\""))
        try:
            rdd.saveAsTextFile(self.dataDirectory + file_name + ".txt")
        except BaseException as e:
            print(e)
        print(file_name)
        time.sleep(1)

    def read_data_from_redis(self):
        university_names = self.redis.get_university_list()
        for name in  university_names:
            data = self.redis.re.lrange(name, 0, -1)

            self.save_data_to_hdfs(data, name)


if __name__ == '__main__':
    hdfs = HDFSStreaming()
    hdfs.read_data_from_redis()



