import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("location-producer:5005")

stub = location_pb2_grpc.LocationServiceStub(channel)


location = location_pb2.LocationMessage(
    longitude="27.5538888222211111", 
    person_id=6,
    latitude="-125.7777666655554444", 
)


response = stub.Create(location)
print(response)