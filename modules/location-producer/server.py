from kafka import KafkaProducer
from concurrent import futures
import location_pb2_grpc
import location_pb2
import json
import grpc
import os
from google.protobuf.json_format import MessageToDict
from models import Location
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
KAFKA_URL = os.environ["KAFKA_URL"]

producer = KafkaProducer(bootstrap_servers=KAFKA_URL)

class LocationService(location_pb2_grpc.LocationServiceServicer):

    def __init__(self, *args, **kwargs):
        engine = create_engine(
            f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        SessionClass = sessionmaker(engine)
        self.session = SessionClass()

        self.TOPIC_NAME = 'locations'
        KAFKA_SERVER = 'kafka:9092'
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

    def Get(self, request, context):

        id = request.id
        location = self.session.query(
            Location).filter(Location.id == id).first()
        print("Location: {}".format(location))
        if location is None:
            return location_pb2.LocationMessage(
                id=id,
                person_id=None,
                longitude=None,
                latitude=None,
                creation_time=None
            )
        else:
            return location_pb2.LocationMessage(**{
                "id": location.id,
                "person_id": location.person_id,
                "longitude": location.longitude,
                "latitude": location.latitude,
                "creation_time": location.creation_time.isoformat(),
            })

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
  location_pb2_grpc.add_LocationServiceServicer_to_server(
      LocationService(), server)
  server.add_insecure_port('[::]:5005')
  server.start()
  server.wait_for_termination()


if __name__ == "__main__":
    serve()