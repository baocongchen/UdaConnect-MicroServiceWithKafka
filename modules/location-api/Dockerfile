FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY ./modules/location-api/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5001

COPY ./modules/location-api .
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]