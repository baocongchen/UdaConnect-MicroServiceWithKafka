FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY ./modules/person-api/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5002

COPY ./modules/person-api .
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5002"]