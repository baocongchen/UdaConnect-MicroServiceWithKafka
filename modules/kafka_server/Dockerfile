FROM python:3.8

WORKDIR .

COPY . .
# RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev
RUN pip3 install -r requirements.txt
RUN python3 -m grpc_tools.protoc -I./app/udaconnect --python_out=./app/udaconnect --grpc_python_out=./app/udaconnect app/udaconnect/location.proto
EXPOSE 5005


CMD ["python3", "server.py"]