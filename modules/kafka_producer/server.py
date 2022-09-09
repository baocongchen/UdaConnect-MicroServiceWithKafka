from kafka import KafkaProducer
from concurrent import futures
import location_pb2_grpc
import location_pb2
import json
import grpc
import os
from google.protobuf.json_format import MessageToDict
import logging

TOPIC_NAME = 'location'
KAFKA_URL = 'kafka-service:9092'

producer = KafkaProducer(bootstrap_servers=KAFKA_URL)

class LocationService(location_pb2_grpc.EventLocationServiceServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):

        request_value = {
            'userId': int(request.userId),
            'latitude': int(request.latitude),
            'longitude': int(request.longitude)
        }
        msg = json.dumps(request_value, indent=2).encode('utf-8')
        producer.send(TOPIC_NAME, msg)
        return location_pb2.EventLocationMessage(**request_value)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
  location_pb2_grpc.add_LocationServiceServicer_to_server(
      LocationService(), server)
  server.add_insecure_port('[::]:5005')
  server.start()
  server.wait_for_termination()


if __name__ == "__main__":
    serve()