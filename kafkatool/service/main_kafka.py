from json import loads
from kafka import KafkaConsumer
from confluent_kafka import Consumer, TopicPartition

bootstrap_servers_property = None


def getTopicList(server_url):
    consumer = Consumer(generate_consumer_parameters(server_url))
    return consumer.list_topics(None, timeout=1).topics


def consume(topic, server_url):
    return KafkaConsumer(
        topic,
        bootstrap_servers=[server_url],
        group_id=topic + 'group',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        consumer_timeout_ms=100,
        value_deserializer=lambda x: loads(x.decode('utf-8')))


def get_kafka_consumer(topic, server_url):
    consumer = Consumer(generate_consumer_parameters(server_url))
    consumer.subscribe([topic])
    return consumer


def generate_consumer_parameters(server_url):
    return {
        'bootstrap.servers': server_url,
        'group.id': 'group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': 'True'
    }


def get_latest_watermark_offset(consumer, topic):
    filtered_topics = consumer.list_topics(topic)
    partitions_dict = filtered_topics.topics[topic].partitions
    offset = 0
    for index in list(partitions_dict.keys()):
        partition = TopicPartition(topic, index)
        partition_offset = consumer.get_watermark_offsets(partition)[1]
        offset = offset + partition_offset
    print("Detected offset for " + topic + " - " + str(offset))
    return offset


def reset_offset(consumer, topic, number):
    latest_offset = get_latest_watermark_offset(consumer, topic)
    target_offset = latest_offset - number
    if target_offset <= 0:
        target_offset = 0
    filtered_topics = consumer.list_topics(topic)
    partitions_dict = filtered_topics.topics[topic].partitions
    for index in list(partitions_dict.keys()):
        partition = TopicPartition(topic, index)
        partition.offset = target_offset
        consumer.assign([partition])
        print("Offset assigned to " + topic + " partition " + str(index) + " " + str(target_offset))

    return consumer


def consumeAll():
    topicList = getTopicList()
    print('Topic count is ' + str(len(topicList)))
    for topic in topicList:
        print('Topic name : ' + topic)
        consume(topic)
