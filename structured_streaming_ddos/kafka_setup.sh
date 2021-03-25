echo "Setup Kafka"
echo "Install Java"
sudo yum install java-1.8.0 -y
sudo yum install python3 -y
python3 -m venv kafka_spark/env
source ~/kafka_spark/env/bin/activate
pip install pip --upgrade
pip install boto3
pip install kafka-python
deactivate


cd /home/ec2-user/
echo "Move Kafka install"

wget https://archive.apache.org/dist/kafka/2.3.1/kafka_2.12-2.3.1.tgz
tar -xzf kafka_2.12-2.2.1.tgz

sudo mv -f kafka_2.12-2.2.1 /opt/kafka
rm kafka_2.12-2.2.1.tgz
export PATH=$PATH:/opt/kafka/bin:/opt/kafka/sbin
sudo yum -y install telnet

echo "Start Zookeeper"
cd /opt/kafka/bin
zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
p_dns=`curl -s  http://169.254.169.254/latest/meta-data/public-hostname`

echo >> /opt/kafka/config/server.properties
echo "advertised.listeners=PLAINTEXT://${p_dns}:9092" >> /opt/kafka/config/server.properties
cd /opt/kafka/bin

echo "Start Kafka"

source kafka-server-start.sh -daemon /opt/kafka/config/server.properties

source kafka-topics.sh --zookeeper localhost:2181 \
  --create \
  --topic logcheck \
  --partitions 2 \
  --replication-factor 1
  
echo "Ensure AWS security group on EC2 server allows port 9092 to be accessible"
