from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql.functions import udf
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession, Row
import pandas as pd
from jedis.jedis import jedis
import time
import json
class HDFSStreamingRead(object):
    def __init__(self):
        # conf = SparkConf().setAppName("SparkStreamingSaving").setMaster("local[*]")
        self.session = SparkSession.builder.appName("SparkStreamingSaving").\
            config("spark.master", "local[*]").getOrCreate()
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
        data_count_df = data_count.toPandas()
        # print(data_count_df)
        # print(data_count_df.shape)
        return data_count_df

    def process(self, time, rdd):
        print("========= %s =========" % str(time))
        print(len(rdd.collect()))
        spark = self.getSparkSessionInstance(rdd.context.getConf())
        if not rdd.isEmpty():
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

                if self.data_all_985 is not None:
                    self.data_all_985 = pd.concat([self.data_all_985, data_985], axis=0)
                    print("all", self.data_all_985.shape)
                    print(self.data_all_985)
                else:
                    self.data_all_985 = data_985
                if self.data_all_c9 is not None:
                    self.data_all_c9 = pd.concat([self.data_all_c9, data_c9], axis=0)
                    print("all:", self.data_all_c9.shape)
                else:
                    self.data_all_c9 = data_c9
                if self.data_all_211 is not None:
                    self.data_all_211 = pd.concat([self.data_all_211, data_211], axis=0)
                    print("211", self.data_all_211.shape)
                else:
                    self.data_all_211 = data_211

                if self.data_all_top is not None:
                    self.data_all_top = pd.concat([self.data_all_top, data_top], axis=0)
                else:
                    self.data_all_top = data_top

                if self.data_all_basic is not None:
                    self.data_all_basic = pd.concat([self.data_all_basic, data_sec], axis=0)
                else:
                    self.data_all_basic = data_sec

                self.calculate_all_data()

            except BaseException as e:
                print(e)
                print(rdd.collect())

    def calculate_all_data(self):
        self.calculate_for_each(self.data_all_c9, 'c9')
        self.calculate_for_each(self.data_all_985, '985')
        self.calculate_for_each(self.data_all_211, '211')
        self.calculate_for_each(self.data_all_top, 'top')
        self.calculate_for_each(self.data_all_basic, 'basic')


    def calculate_for_each(self, data_df, type):
        if data_df.shape[0] != 0:
            data_df['count'] = data_df['count'].astype(float)
            data_df = data_df.groupby(['date']).mean().reset_index()
            date = data_df['date'].values
            date_time = list(map(lambda x: get_mktime(x), date))
            data_df['time_stamp'] = date_time
            data_df.sort_values(by=['time_stamp'], inplace=True, ascending=True)
            data_df['type'] = type
            data_df.to_csv('../data/' + type + '_date_number.csv')


    def calculate_date_for_all(self, data):
        pass


# 将字符串时间转换为时间戳
def get_mktime(date_string):
    return time.mktime(time.strptime(date_string, '%Y-%m-%d'))


if __name__ =="__main__":
    hdfs = HDFSStreamingRead()
    hdfs.analysis_data()
    hdfs.monitor_data()