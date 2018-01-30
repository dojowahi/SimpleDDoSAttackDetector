# Simple DDoS detector using Spark Streaming

### Prerequisite
Spark Streaming (Python API)
Apache Flume (Python API)
Python 2.7 or above
HDP 2.5

### Purpose
The goal is get better understanding of Spark streaming's windowing functions
Description
The Spark code identifies potential IPs from which a DDOS attack orginates within a minute of the attack.


### Apache log message sample
155.156.168.116 - - [25/May/2015:23:11:15 +0000] "GET / HTTP/1.0" 200 3557 "-" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; acc=baadshah; acc=none; freenet DSL 1.1; (none))"
For more information, please read the apache log format.

### Execution Steps


The steps to test this code are as follows:

1) Start Flume in HDP with following command, make sure you change the directories based on your env.


```bin/flume-ng agent --conf conf --conf-file /home/maria_dev/flume/sparkstreamingflume.conf --name a1```

2) Execute the Spark job as shown below


```spark-submit --packages org.apache.spark:spark-streaming-flume_2.11:2.0.0 SparkFlumeIpPh.py```

3) Start feeding log data to Flume Spool directory based on your env

### Future steps
Implement more Machine Learning to detect DDOS attackers.
