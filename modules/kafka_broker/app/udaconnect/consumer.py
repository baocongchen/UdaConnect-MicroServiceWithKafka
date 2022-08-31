from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

import location_pb2_grpc
import grpc
import os
from google.protobuf.json_format import MessageToDict
import logging

def launch_consumer():
    KAFKA_SERVER = 'kafka-consumer.default.svc.cluster.local'
    TOPIC_NAME = "locations"

    logging.info(f"Connecting to Kafka at {KAFKA_SERVER}")
    
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)
    channel = grpc.insecure_channel("127.0.0.1:5006", options=(('grpc.enable_http_proxy', 0),))
    stub = location_pb2_grpc.LocationServiceStub(channel)
    while True:
        try:
            for msg in consumer:
                location_dict = MessageToDict(msg.value)
                stub.Create(location_dict)
                logging.info(f"Created Location object: {location_dict}")
        except:
            print("Unexected error occurred")
        finally:
            consumer.close()


if __name__ == "__main__":
    launch_consumer()