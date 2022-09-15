import grpc
import location_pb2
import location_pb2_grpc
import sys
"""
Sample implementation of a getter that can be used to receive gRPC messages.
"""

print("Sending sample payload...")
location_id = sys.argv[-1]
channel = grpc.insecure_channel(
    "location-producer:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

response = stub.Get(location_pb2.LocationID(id=location_id))
print(response)