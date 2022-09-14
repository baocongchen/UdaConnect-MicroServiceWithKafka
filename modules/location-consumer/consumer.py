from kafka import KafkaConsumer
from sqlalchemy import create_engine
import json
import os
TOPIC_NAME = "location"
print('started listening ' + TOPIC_NAME)

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
KAFKA_URL = os.environ["KAFKA_URL"]

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