FROM python:3.8

WORKDIR .

COPY ./modules/location-producer .
# RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto
EXPOSE 5005


CMD ["python3", "server.py"]