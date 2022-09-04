FROM python:3.8
WORKDIR .
COPY . .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5004
CMD ["python", "consumer.py"]