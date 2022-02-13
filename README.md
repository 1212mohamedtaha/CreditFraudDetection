# Credit Card Fraud Detection

In this project, we present a semi-supervised approach to detect credit card fraud in real-time. And 
implemented a whole data pipeline and data visualization dashboard to monitor transactions and 
fraud alerts, as well as the model performance.

## Training

Download the data from Kaggle from this [link](https://www.kaggle.com/mlg-ulb/creditcardfraud) 

Run the thr app/train.ipynp notebook

In training, We implemented a semi-supervised learning approach. 

## Deployment Requirements:
- Kafaka Server
- PostgreSQL Database
- Data visualization tool (ex. Grafana, Tableau, Power BI)


You can use docker images for Kafka and Zookeeper from DockerHub
we used wurstmeister/kafka, wurstmeister/zookeeper

Use the official PostgreSQL Docker image or use the Azure PostgreSQL service

### Set Up the PostgreSQL Database
### Set Up Kafka


```bash
cd kafka
docker-compose up
```
In the kafka terminal:
```bash
#Create a topic
kafka-topics.sh --zookeeper zookeeper1:2181/kafka --create --topic test 
--replication-factor 1 --partitions
```
### Open a terminal and run cons.py 

### In another terminal: Run prod.py

### In another terminal: Run prod.py
### Connect the database to your Grafana or Power BI and create your dashboard. 

You can also run the model inside a docker container by running app/Dockerfile

