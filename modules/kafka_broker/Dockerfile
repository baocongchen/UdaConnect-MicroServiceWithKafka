FROM python:3.8

WORKDIR .

# RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev
COPY ./modules/kafka_broker/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./modules/kafka_broker/app/udaconnect/location.proto app/udaconnect/location.proto
RUN python3 -m grpc_tools.protoc -I./app/udaconnect --python_out=./app/udaconnect --grpc_python_out=./app/udaconnect app/udaconnect/location.proto
EXPOSE 5004

COPY ./modules/kafka_broker .
CMD ["python3", "app/udaconnect/consumer.py"]