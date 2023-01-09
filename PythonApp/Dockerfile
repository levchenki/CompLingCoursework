FROM openjdk:8-bullseye

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip install numpy
RUN pip install pyspark redis pymongo pymorphy2 flask

WORKDIR /app
COPY . .

CMD ["python3", "main.py"]