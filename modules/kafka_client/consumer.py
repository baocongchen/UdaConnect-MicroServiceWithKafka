from kafka import KafkaConsumer
from sqlalchemy import create_engine
import os
import json

TOPIC_NAME = "location"
print('started listening ' + TOPIC_NAME)

DB_USERNAME = "ct_geoconnections"
DB_PASSWORD = "d293aW1zb3NlY3VyZQ=="
DB_HOST = "postgres-geoconnections"
DB_PORT = 5432
DB_NAME = "geoconnections"
KAFKA_URL = "kafka-service:9092"

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_URL])

def save_location(location):
    engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
    conn = engine.connect()

    person_id = int(location["userId"])
    latitude, longitude = int(location["latitude"]), int(location["longitude"])

    insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))" \
        .format(person_id, latitude, longitude)

    print(insert)
    conn.execute(insert)

while True:
    for location in consumer:
        message = location.value.decode('utf-8')
        print('{}'.format(message))
        location_message = json.loads(message)
        save_location(location_message)