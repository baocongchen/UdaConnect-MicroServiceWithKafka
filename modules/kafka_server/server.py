from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

import location_pb2_grpc
import grpc
import os
from google.protobuf.json_format import MessageToDict
import logging

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
      RouteGuideServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()


if __name__ == "__main__":
    serve()