from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession, Row
import json
class HDFSStreamingRead(object):
    def __init__(self):
        # conf = SparkConf().setAppName("SparkStreamingSaving").setMaster("local[*]")
        self.session = SparkSession.builder.appName("SparkStreamingSaving").config("spark.master", "local[*]").getOrCreate()
        self.sc = self.session.sparkContext
        self.streamContext = StreamingContext(self.sc, 2)
        self.dataDirectory = "hdfs://localhost:9000/user/maicius/test_data/"
        self.outputDirectory = "/Users/maicius/code/ShowQQ/result/"

    def monitor_data(self):
        self.streamContext.start()
        self.streamContext.awaitTerminationOrTimeout(timeout=1000)

    def analysis_data(self):
        data = self.streamContext.textFileStream(self.dataDirectory)
        data_rdds =  data.flatMap(lambda line: line.split(" "))
        data_rdds.foreachRDD(process)

def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']

def process(time, rdd):
    print("========= %s =========" % str(time))
    spark = getSparkSessionInstance(rdd.context.getConf())
    rowRdd = rdd.map(lambda w: Row(word=w))
    data_df = spark.createDataFrame(rowRdd)
    # rdd.pprint(20)
    data_df.show()
    print(rdd.collect())

if __name__ =="__main__":
    hdfs = HDFSStreamingRead()
    hdfs.analysis_data()
    hdfs.monitor_data()