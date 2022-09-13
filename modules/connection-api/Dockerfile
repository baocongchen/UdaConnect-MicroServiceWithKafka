FROM python:3.8

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY ./modules/connection-api/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5003

COPY ./modules/connection-api .
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5003"]