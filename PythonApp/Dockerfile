FROM openjdk:8-bullseye

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip install numpy
RUN pip install pyspark pymorphy3 nltk
RUN pip install fastapi uvicorn
RUN pip install beanie motor lxml beautifulsoup4 asyncio pandas

RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader averaged_perceptron_tagger_ru
RUN python3 -m nltk.downloader stopwords

WORKDIR /app
#COPY . .

CMD ["python3", "main.py"]