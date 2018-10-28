from pyspark import SparkConf
from pyspark import SparkContext
import datetime
import json
from constant.constant import UNIVERSITY_INFO
import time
import redis

class HDFSStreaming(object):
    def __init__(self):
        conf = SparkConf().setAppName("SparkStreamingSaving").setMaster("local[*]")
        self.sc = SparkContext.getOrCreate(conf)
        self.dataDirectory = "hdfs://localhost:9000/user/maicius/test_data/"
        self.redis = self.get_re()

    def get_re(self):
        try:
            pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
            return redis.StrictRedis(connection_pool=pool)
        except BaseException as e:
            print(e)

    def save_data_to_hdfs(self, data, data_type):
        timestamp = time.mktime(datetime.datetime.now().timetuple())
        rdd = self.sc.parallelize(data)
        rdd = rdd.map(lambda x: json.loads(x.replace("\'", "\""))).map(lambda x: x['company_name'] + "==" + x['date'] + "==" + data_type)
        try:
            print(len(rdd.collect()))
            rdd.saveAsTextFile(self.dataDirectory + str(timestamp) + ".txt")
        except BaseException as e:
            print(e)
        print(timestamp)
        time.sleep(1)

    def read_data_from_redis(self):
        university_names = UNIVERSITY_INFO.keys()
        for name in  university_names:
            table = name + "_company_info"
            data = self.redis.lrange(table, 0, -1)
            data_type = UNIVERSITY_INFO[name][1] + "==" + UNIVERSITY_INFO[name][3]
            self.save_data_to_hdfs(data, data_type)


if __name__ == '__main__':
    hdfs = HDFSStreaming()
    hdfs.read_data_from_redis()



