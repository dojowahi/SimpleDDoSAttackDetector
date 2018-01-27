The code was tested on HDP 2.5.
The steps to test this code are as follows:

1) Start Flume in HDP with following command, make sure you change the directories based on your env.
bin/flume-ng agent --conf conf --conf-file /home/maria_dev/flume/sparkstreamingflume.conf --name a1

2) Execute the Spark job as shown below
spark-submit --packages org.apache.spark:spark-streaming-flume_2.11:2.0.0 SparkFlumeIpPh.py

3) Start feeding log data to Flume Spool directory based on your env