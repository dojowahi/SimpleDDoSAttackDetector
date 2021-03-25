import re

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.flume import FlumeUtils

parts = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',               # referer "%{Referer}i"
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]
pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

def extractHost(line):
    exp = pattern.match(line)
    if exp:
        host = exp.groupdict()["host"]
        if host:
            return host


if __name__ == "__main__":

    sc = SparkContext(appName="StreamingFlumeLogAggregator")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 5)

    flumeStream = FlumeUtils.createStream(ssc, "localhost", 9092)

    lines = flumeStream.map(lambda x: x[1])
    hostIp = lines.map(extractHost)


    #hostCounts = hostIp.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)

    hostCounts = hostIp.map(lambda x: (x, 1)).reduceByKeyAndWindow(lambda x, y: x + y, lambda x, y : x - y, 60, 10)
    # Sort and print the results
    sortedResults = hostCounts.transform(lambda rdd: rdd.sortBy(lambda x: x[1], False))
    #sortedResults.pprint()
    sortedResults.saveAsTextFiles("hdfs:///home/maria_dev/logs/DDoS_Attack_List_Sorted")
    hostSuspicious=hostCounts.filter(lambda x: x[1] >50)
    hostSuspicious.pprint()
    hostSuspicious.count()
    hostSuspicious.saveAsTextFiles("hdfs:///home/maria_dev/logs/DDoS_Suspicious")

    ssc.checkpoint("/home/maria_dev/checkpoint")
    ssc.start()
    ssc.awaitTermination()
