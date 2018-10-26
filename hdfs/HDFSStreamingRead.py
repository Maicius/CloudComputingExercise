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
        self.streamContext = StreamingContext(self.sc, 3)
        self.dataDirectory = "hdfs://localhost:9000/user/maicius/test_data/"
        self.outputDirectory = "/Users/maicius/code/ShowQQ/result/"
        self.data_all_985 = None
        self.data_all_211 = None
        self.data_all_top = None
        self.data_all_c9 = None
        self.data_all_basic = None

    def monitor_data(self):
        self.streamContext.start()
        self.streamContext.awaitTerminationOrTimeout(timeout=1000)

    def analysis_data(self):
        data = self.streamContext.textFileStream(self.dataDirectory)
        data_rdds =  data.flatMap(lambda line: line.split(" "))
        data_rdds.foreachRDD(self.process)

    def getSparkSessionInstance(self, sparkConf):
        if ('sparkSessionSingletonInstance' not in globals()):
            globals()['sparkSessionSingletonInstance'] = SparkSession \
                .builder \
                .config(conf=sparkConf) \
                .getOrCreate()
        return globals()['sparkSessionSingletonInstance']

    def process_data_by_type(self, data, type):
        # data.select('type').show()
        data_type = data.filter(data['type'] == type)
        print("筛选type:", type)
        data_count = data_type.groupBy("date").count()
        print(data_count.show())
        return data_type

    def accumulate_data(self):
        pass

    def process(self, time, rdd):
        print("========= %s =========" % str(time))
        spark = self.getSparkSessionInstance(rdd.context.getConf())
        size = len(rdd.collect())
        print(size)
        if size > 0:
            rdd = rdd.map(lambda x: x.split("=="))
            try:
                rdd = rdd.filter(lambda x: len(x) == 4)
                print("数据清理...")
                rowRdd = rdd.map(lambda x: Row(company=x[0], date=x[1], type=x[2], city=x[3]))
                data_df = spark.createDataFrame(rowRdd)
                data_c9 = self.process_data_by_type(data_df, "C9")
                data_985 = self.process_data_by_type(data_df, "985")
                data_211 = self.process_data_by_type(data_df, "211")
                data_top = self.process_data_by_type(data_df, "一本")
                data_sec = self.process_data_by_type(data_df, "二本")
            except BaseException as e:
                print(e)
                print(rdd.collect())


if __name__ =="__main__":
    hdfs = HDFSStreamingRead()
    hdfs.analysis_data()
    hdfs.monitor_data()