from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

import location_pb2_grpc
import grpc
import os
from google.protobuf.json_format import MessageToDict
import logging

def launch_consumer():

    kafka_uri = "localhost:9092"
    TOPIC_NAME = "locations"

    logging.info(f"Connecting to Kafka at {kafka_uri}")

    try:
        consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=kafka_uri)
        channel = grpc.insecure_channel("127.0.0.1:5006", options=(('grpc.enable_http_proxy', 0),))
        stub = location_pb2_grpc.LocationServiceStub(channel)
        try:
            for msg in consumer:
                location_dict = MessageToDict(msg.value)
                stub.Create(location_dict)
                logging.info(f"Created Location object: {location_dict}")
        except:
            print("Unexected error occurred")
        finally:
            consumer.close()
    except NoBrokersAvailable as err:
        print(f"Failed to establish a connection. Error: {err}")
        logging.info(f"Failed to establish a connection. Error: {err}")


if __name__ == "__main__":
    launch_consumer()