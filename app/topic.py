from kafka.admin import KafkaAdminClient, NewTopic

try:
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092", 
        client_id='test'
    )

    topic_list = []
    topic_list.append(NewTopic(name='top1', num_partitions=1, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    print (topic_list, "Created")
except Exception as  e:
    print(e)