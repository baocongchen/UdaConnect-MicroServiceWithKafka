import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a getter that can be used to receive gRPC messages.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("location-producer:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

response = stub.Get(location_pb2.LocationID(id=29))
print(response)