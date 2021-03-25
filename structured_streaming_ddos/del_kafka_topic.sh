sh /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic logcheck --delete 
sleep 10
sh  /opt/kafka/bin/kafka-topics.sh --zookeeper localhost:2181   --create   --topic logcheck   --partitions 2   --replication-factor 1
